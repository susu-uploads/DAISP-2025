from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from PIL import Image
import network
import uvicorn
import io
import pickle
import uuid
import os
import glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Временное хранилище для изображений
temp_images_storage = {}

class FeedbackRequest(BaseModel):
    prediction_id: str
    is_correct: bool
    answer: int

def load_network() -> network.Network:
    net = network.Network([784, 128, 64, 32, 10])
    with open('./weights.pkl', 'rb') as f:
        data = pickle.load(f)
        net.weights = data['weights']
        net.biases = data['biases']
    return net

def save_network(net):
    with open('./weights.pkl', 'wb') as f:
        pickle.dump({'weights': net.weights, 'biases': net.biases}, f)

def save_prediction(image, prediction, filename):
    os.makedirs(f'./predictions_data/{prediction}', exist_ok=True)
    save_path = f'./predictions_data/{prediction}/{filename}'
    image.save(save_path)

def predict_digit(image):
    image_gray = image.convert('L').resize((28, 28))
    pixels = list(image_gray.getdata())
    target = np.array(pixels).reshape(784, 1) / 255.0
    output = net.feedforward(target)
    return int(np.argmax(output))

net = load_network()

@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")
    
    try:
        contents = await file.read()        
        image = Image.open(io.BytesIO(contents))
        prediction = str(predict_digit(image))
    
        prediction_id = str(uuid.uuid4())        
        temp_images_storage[prediction_id] = {
            'image': image,
            'prediction': prediction,
            'filename': file.filename
        }
        
        return {
            "prediction_id": prediction_id,
            "filename": file.filename,
            "prediction": prediction
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обработки изображения: {str(e)}")


@app.post("/api/v1/feedback")
async def feedback(request: FeedbackRequest):
    if request.prediction_id not in temp_images_storage:
        raise HTTPException(status_code=404, detail="Предсказание не найдено")
    
    image_data = temp_images_storage[request.prediction_id]
    
    if request.is_correct:
        save_prediction(
            image_data['image'], 
            image_data['prediction'], 
            image_data['filename']
        )
        message = "Изображение сохранено"
    else:
        save_prediction(
            image_data['image'],
            request.answer,
            image_data['filename']
        )
        message = "Ошибка отмечена, изображение сохранено"
    
    # Удаляем из временного хранилища
    del temp_images_storage[request.prediction_id]
    
    return {"message": message}

@app.post("/api/v1/train")
async def train():
    training_data = []
    
    # Проходим по всем папкам с цифрами
    for digit in range(10):
        digit_path = f'./predictions_data/{digit}/*'
        for image_path in glob.glob(digit_path):
            # Загружаем и обрабатываем изображение
            image = Image.open(image_path)
            image_gray = image.convert('L').resize((28, 28))
            pixels = list(image_gray.getdata())
            x = np.array(pixels).reshape(784, 1) / 255.0
            
            # Создаем one-hot вектор для метки
            y = np.zeros((10, 1))
            y[digit] = 1.0
            
            training_data.append((x, y))
    
    if not training_data:
        raise HTTPException(status_code=400, detail="Нет данных для обучения")
    
    mini_batch_size = 10
    if len(training_data) < mini_batch_size:
        mini_batch_size = len(training_data)
    net.SGD(training_data, epochs=40, mini_batch_size=mini_batch_size, eta=3.0)
    
    # Сохраняем обновленные веса
    save_network(net)
    
    return {"message": f"Модель дообучена на {len(training_data)} изображениях"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
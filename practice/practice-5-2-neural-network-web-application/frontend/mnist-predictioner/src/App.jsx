import { useState } from 'react';
import { Upload, Send, CheckCircle, XCircle, Brain } from 'lucide-react';

export default function App() {
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [predictionId, setPredictionId] = useState(null);
    const [showFeedback, setShowFeedback] = useState(false);
    const [showCorrection, setShowCorrection] = useState(false);
    const [correctAnswer, setCorrectAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
            setPrediction(null);
            setShowFeedback(false);
            setShowCorrection(false);
            setMessage('');
        }
    };

    const handlePredict = async () => {
        if (!image) {
            setMessage('Пожалуйста, загрузите изображение');
            return;
        }

        setLoading(true);
        setMessage('');

        const formData = new FormData();
        formData.append('file', image);

        try {
            const response = await fetch('http://localhost:8000/api/v1/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Ошибка предсказания');

            const data = await response.json();
            setPrediction(data.prediction || data.result || JSON.stringify(data));
            setPredictionId(data.prediction_id);
            setShowFeedback(true);
            setShowCorrection(false);
        } catch (error) {
            setMessage(`Ошибка: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleCorrectFeedback = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prediction_id: predictionId,
                    is_correct: true,
                    answer: prediction
                })
            });

            if (!response.ok) throw new Error('Ошибка отправки обратной связи');

            setMessage('Спасибо за обратную связь!');
            setShowFeedback(false);
        } catch (error) {
            setMessage(`Ошибка: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleIncorrectFeedback = () => {
        setShowCorrection(true);
    };

    const handleSendCorrection = async () => {
        if (!correctAnswer.trim()) {
            setMessage('Пожалуйста, введите правильный ответ');
            return;
        }

        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prediction_id: predictionId,
                    is_correct: false,
                    answer: parseInt(correctAnswer)
                })
            });

            if (!response.ok) throw new Error('Ошибка отправки обратной связи');

            setMessage('Спасибо за исправление!');
            setShowFeedback(false);
            setShowCorrection(false);
            setCorrectAnswer('');
        } catch (error) {
            setMessage(`Ошибка: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleTrain = async () => {
        setLoading(true);
        setMessage('');
        try {
            const response = await fetch('http://localhost:8000/api/v1/train', {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Ошибка дообучения модели');

            setMessage('Дообучение модели запущено успешно!');
        } catch (error) {
            setMessage(`Ошибка: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-8">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
                    Предсказание по изображению
                </h1>

                {/* Image Upload Area */}
                <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <label
                        htmlFor="image-upload"
                        className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-400 transition-colors"
                    >
                        {imagePreview ? (
                            <img
                                src={imagePreview}
                                alt="Preview"
                                className="max-h-full max-w-full object-contain"
                            />
                        ) : (
                            <div className="flex flex-col items-center">
                                <Upload className="w-12 h-12 text-gray-400 mb-3" />
                                <p className="text-sm text-gray-600">Нажмите для загрузки изображения</p>
                            </div>
                        )}
                        <input
                            id="image-upload"
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="hidden"
                        />
                    </label>

                    {/* Predict Button */}
                    <button
                        onClick={handlePredict}
                        disabled={!image || loading}
                        className="w-full mt-4 bg-blue-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                    >
                        {loading ? 'Обработка...' : (
                            <>
                                <Send className="w-5 h-5" />
                                Предсказать
                            </>
                        )}
                    </button>
                </div>

                {/* Prediction Result */}
                {prediction && (
                    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                        <h2 className="text-lg font-semibold mb-3 text-gray-700">Результат предсказания:</h2>
                        <p className="text-xl font-bold text-blue-600 mb-4">{prediction}</p>

                        {showFeedback && !showCorrection && (
                            <div className="flex gap-3">
                                <button
                                    onClick={handleCorrectFeedback}
                                    disabled={loading}
                                    className="flex-1 bg-green-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-600 disabled:bg-gray-300 transition-colors flex items-center justify-center gap-2"
                                >
                                    <CheckCircle className="w-5 h-5" />
                                    Верно
                                </button>
                                <button
                                    onClick={handleIncorrectFeedback}
                                    disabled={loading}
                                    className="flex-1 bg-red-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-600 disabled:bg-gray-300 transition-colors flex items-center justify-center gap-2"
                                >
                                    <XCircle className="w-5 h-5" />
                                    Не верно
                                </button>
                            </div>
                        )}

                        {showCorrection && (
                            <div className="mt-4">
                                <input
                                    type="text"
                                    value={correctAnswer}
                                    onChange={(e) => setCorrectAnswer(e.target.value)}
                                    placeholder="Введите правильный ответ"
                                    className="w-full p-3 border border-gray-300 rounded-lg mb-3 focus:outline-none focus:border-blue-400"
                                />
                                <button
                                    onClick={handleSendCorrection}
                                    disabled={loading}
                                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-300 transition-colors"
                                >
                                    Отправить исправление
                                </button>
                            </div>
                        )}
                    </div>
                )}

                {/* Status Message */}
                {message && (
                    <div className={`mb-6 p-4 rounded-lg ${message.includes('Ошибка')
                        ? 'bg-red-100 text-red-700'
                        : 'bg-green-100 text-green-700'
                        }`}>
                        {message}
                    </div>
                )}

                {/* Train Model Button */}
                <button
                    onClick={handleTrain}
                    disabled={loading}
                    className="w-full bg-purple-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-purple-600 disabled:bg-gray-300 transition-colors flex items-center justify-center gap-2"
                >
                    {loading ? 'Обработка...' : (
                        <>
                            <Brain className="w-5 h-5" />
                            Дообучить модель
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}
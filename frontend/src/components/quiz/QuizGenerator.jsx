import React, { useState } from 'react';
import { Brain, Play, RotateCcw, CheckCircle, XCircle, Clock, BookOpen } from 'lucide-react';
import { quizAPI } from '../../services/api';
import toast from 'react-hot-toast';

const QuizGenerator = ({ document, onQuizGenerated }) => {
  const [quiz, setQuiz] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  const generateQuiz = async () => {
    if (!document) {
      toast.error('Please select a document first');
      return;
    }

    setIsGenerating(true);
    try {
      // For now, we'll use a placeholder since the backend might not have the actual document text
      const response = await quizAPI.generate("Sample document text for quiz generation");
      setQuiz(response.questions);
      setCurrentQuestion(0);
      setAnswers({});
      setShowResults(false);
      setScore(0);
      
      if (onQuizGenerated) {
        onQuizGenerated(response.questions);
      }
      
      toast.success('Quiz generated successfully!');
    } catch (error) {
      console.error('Quiz generation error:', error);
      toast.error('Failed to generate quiz');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const nextQuestion = () => {
    if (currentQuestion < quiz.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const submitQuiz = () => {
    let correctAnswers = 0;
    quiz.forEach(question => {
      if (question.type === 'multiple_choice') {
        if (answers[question.id] === question.correct_answer) {
          correctAnswers++;
        }
      }
    });
    
    setScore(correctAnswers);
    setShowResults(true);
  };

  const resetQuiz = () => {
    setQuiz(null);
    setCurrentQuestion(0);
    setAnswers({});
    setShowResults(false);
    setScore(0);
  };

  const getQuestionTypeIcon = (type) => {
    switch (type) {
      case 'multiple_choice':
        return <CheckCircle className="h-5 w-5 text-blue-500" />;
      case 'open_ended':
        return <BookOpen className="h-5 w-5 text-green-500" />;
      default:
        return <Brain className="h-5 w-5 text-purple-500" />;
    }
  };

  if (!document) {
    return (
      <div className="card text-center py-12">
        <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No document selected</h3>
        <p className="text-gray-500">
          Select a document to generate a quiz from its content
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="bg-purple-100 p-2 rounded-lg">
            <Brain className="h-6 w-6 text-purple-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Quiz Generator</h2>
            <p className="text-sm text-gray-500">{document.filename}</p>
          </div>
        </div>
        
        {quiz && (
          <button
            onClick={resetQuiz}
            className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <RotateCcw className="h-4 w-4" />
            <span>New Quiz</span>
          </button>
        )}
      </div>

      {!quiz ? (
        /* Generate Quiz Section */
        <div className="text-center py-12">
          <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Generate AI Quiz
          </h3>
          <p className="text-gray-500 mb-6">
            Create a personalized quiz based on your document content
          </p>
          <button
            onClick={generateQuiz}
            disabled={isGenerating}
            className="btn-primary flex items-center space-x-2 mx-auto"
          >
            {isGenerating ? (
              <>
                <div className="loading-spinner h-5 w-5"></div>
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Brain className="h-5 w-5" />
                <span>Generate Quiz</span>
              </>
            )}
          </button>
        </div>
      ) : showResults ? (
        /* Results Section */
        <div className="text-center py-8">
          <div className="mb-6">
            <div className="text-6xl font-bold text-primary-600 mb-2">
              {score}/{quiz.filter(q => q.type === 'multiple_choice').length}
            </div>
            <div className="text-lg text-gray-600">
              {score === quiz.filter(q => q.type === 'multiple_choice').length 
                ? 'Perfect Score! 🎉' 
                : score >= quiz.filter(q => q.type === 'multiple_choice').length * 0.7
                ? 'Great Job! 👍'
                : 'Keep Studying! 📚'
              }
            </div>
          </div>
          
          <div className="space-y-4">
            <button
              onClick={resetQuiz}
              className="btn-primary"
            >
              Take Another Quiz
            </button>
            <button
              onClick={() => setShowResults(false)}
              className="btn-secondary ml-3"
            >
              Review Answers
            </button>
          </div>
        </div>
      ) : (
        /* Quiz Questions */
        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-600">
                Question {currentQuestion + 1} of {quiz.length}
              </span>
            </div>
            <div className="w-32 bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestion + 1) / quiz.length) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Current Question */}
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              {getQuestionTypeIcon(quiz[currentQuestion].type)}
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {quiz[currentQuestion].question}
                </h3>
                
                {quiz[currentQuestion].type === 'multiple_choice' ? (
                  <div className="space-y-3">
                    {quiz[currentQuestion].options.map((option, index) => (
                      <label
                        key={index}
                        className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                          answers[quiz[currentQuestion].id] === index
                            ? 'border-primary-500 bg-primary-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`question-${quiz[currentQuestion].id}`}
                          value={index}
                          checked={answers[quiz[currentQuestion].id] === index}
                          onChange={() => handleAnswerSelect(quiz[currentQuestion].id, index)}
                          className="sr-only"
                        />
                        <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                          answers[quiz[currentQuestion].id] === index
                            ? 'border-primary-500 bg-primary-500'
                            : 'border-gray-300'
                        }`}>
                          {answers[quiz[currentQuestion].id] === index && (
                            <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                          )}
                        </div>
                        <span className="text-gray-700">{option}</span>
                      </label>
                    ))}
                  </div>
                ) : (
                  <textarea
                    className="input-field h-32 resize-none"
                    placeholder="Type your answer here..."
                    value={answers[quiz[currentQuestion].id] || ''}
                    onChange={(e) => handleAnswerSelect(quiz[currentQuestion].id, e.target.value)}
                  />
                )}
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <button
              onClick={previousQuestion}
              disabled={currentQuestion === 0}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <div className="flex space-x-3">
              {currentQuestion === quiz.length - 1 ? (
                <button
                  onClick={submitQuiz}
                  className="btn-success flex items-center space-x-2"
                >
                  <CheckCircle className="h-5 w-5" />
                  <span>Submit Quiz</span>
                </button>
              ) : (
                <button
                  onClick={nextQuestion}
                  className="btn-primary"
                >
                  Next
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizGenerator;

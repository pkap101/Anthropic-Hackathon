import React, { useState } from 'react';
import { Send, Sparkles, BookOpen, GraduationCap, RefreshCw } from 'lucide-react';

const AutoGrader = () => {
  const [course, setCourse] = useState('dmt_2');
  const [question, setQuestion] = useState('');
  const [studentAnswer, setStudentAnswer] = useState('');
  const [rubric, setRubric] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [showExamples, setShowExamples] = useState(false);

  const API_URL = 'http://localhost:8000/api/grader'; // Update with your actual API URL

  const handleSubmit = async () => {
    if (!question || !studentAnswer || !rubric) {
      setResult('⚠️ Please fill in all fields before grading.');
      return;
    }

    setLoading(true);
    setResult('');

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          student_answer: studentAnswer,
          rubric,
          course,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const formatted = `${data.response || 'No response received'}\n\n---\n📊 Tokens used: ${data.tokens_used || 'N/A'} | Model: ${data.model || 'N/A'}`;
      setResult(formatted);
    } catch (error) {
      console.error('Error calling API:', error);
      setResult(`❌ Sorry, I couldn't connect to the backend service. Please check if the API is running at ${API_URL}.\n\nError: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    setStudentAnswer('');
    setRubric('');
    setResult('');
  };

  const loadExample = (exampleNum) => {
    if (exampleNum === 1) {
      setQuestion('What is the capital of France?');
      setStudentAnswer('Paris is the capital of France.');
      setRubric('1 point for correct answer. 0 points for incorrect answer.');
    } else if (exampleNum === 2) {
      setQuestion('Explain the difference between supervised and unsupervised learning.');
      setStudentAnswer('Supervised learning uses labeled data while unsupervised learning finds patterns in unlabeled data.');
      setRubric('Full credit (5 pts): Clear explanation of both concepts with examples. Partial credit (3 pts): Mentions key difference but lacks detail. No credit (0 pts): Incorrect or missing explanation.');
    }
    setShowExamples(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 text-slate-100">
      {/* Animated background effect */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 mb-4 shadow-lg shadow-indigo-500/50">
            <GraduationCap className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-200 via-violet-200 to-indigo-200 bg-clip-text text-transparent mb-3">
            Auto Grader
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Enter the question, student answer, and rubric to receive automated grading feedback powered by AI
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Inputs */}
          <div className="space-y-6">
            {/* Course Selection */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl">
              <label className="block text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                Course
              </label>
              <select
                value={course}
                onChange={(e) => setCourse(e.target.value)}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              >
                <option value="dmt_2">DMT 2</option>
                <option value="qa">QA</option>
              </select>
            </div>

            {/* Question */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl">
              <label className="block text-sm font-semibold text-slate-300 mb-3">
                Question
              </label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter the question here..."
                rows={3}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
              />
            </div>

            {/* Student Answer */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl">
              <label className="block text-sm font-semibold text-slate-300 mb-3">
                Student Answer
              </label>
              <textarea
                value={studentAnswer}
                onChange={(e) => setStudentAnswer(e.target.value)}
                placeholder="Enter the student's answer here..."
                rows={5}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
              />
            </div>

            {/* Rubric */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl">
              <label className="block text-sm font-semibold text-slate-300 mb-3">
                Rubric
              </label>
              <textarea
                value={rubric}
                onChange={(e) => setRubric(e.target.value)}
                placeholder="Enter the grading rubric here..."
                rows={5}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    Grading...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Grade
                  </>
                )}
              </button>
              <button
                onClick={handleClear}
                className="px-6 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-xl border border-slate-700 transition-all"
              >
                Clear
              </button>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {/* Grading Result */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl min-h-[400px]">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-indigo-400" />
                <h3 className="text-xl font-bold text-slate-200">Grading Result</h3>
              </div>
              <div className="prose prose-invert prose-slate max-w-none">
                {result ? (
                  <div className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result}
                  </div>
                ) : (
                  <div className="text-slate-500 text-center py-12">
                    <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-slate-800/50 mb-4">
                      <Sparkles className="w-6 h-6 text-slate-600" />
                    </div>
                    <p>Grading result will appear here...</p>
                  </div>
                )}
              </div>
            </div>

            {/* Examples Section */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50 shadow-xl">
              <button
                onClick={() => setShowExamples(!showExamples)}
                className="w-full flex items-center justify-between text-left mb-4 group"
              >
                <span className="text-lg font-semibold text-slate-200 group-hover:text-indigo-300 transition-colors">
                  💡 Example Questions
                </span>
                <span className="text-slate-400 text-sm">
                  {showExamples ? 'Click to hide' : 'Click to expand'}
                </span>
              </button>

              {showExamples && (
                <div className="space-y-6 animate-in fade-in slide-in-from-top-2 duration-300">
                  {/* Example 1 */}
                  <div className="border-l-4 border-indigo-500 pl-4 py-2">
                    <h4 className="font-semibold text-slate-200 mb-2">Example 1: Simple Factual Question</h4>
                    <div className="text-sm text-slate-400 space-y-1 mb-3">
                      <p><strong className="text-slate-300">Question:</strong> What is the capital of France?</p>
                      <p><strong className="text-slate-300">Student Answer:</strong> Paris is the capital of France.</p>
                      <p><strong className="text-slate-300">Rubric:</strong> 1 point for correct answer. 0 points for incorrect answer.</p>
                    </div>
                    <button
                      onClick={() => loadExample(1)}
                      className="text-sm px-4 py-2 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 rounded-lg border border-indigo-500/30 transition-all"
                    >
                      📋 Use Example 1
                    </button>
                  </div>

                  {/* Example 2 */}
                  <div className="border-l-4 border-violet-500 pl-4 py-2">
                    <h4 className="font-semibold text-slate-200 mb-2">Example 2: Explanation Question</h4>
                    <div className="text-sm text-slate-400 space-y-1 mb-3">
                      <p><strong className="text-slate-300">Question:</strong> Explain the difference between supervised and unsupervised learning.</p>
                      <p><strong className="text-slate-300">Student Answer:</strong> Supervised learning uses labeled data while unsupervised learning finds patterns in unlabeled data.</p>
                      <p><strong className="text-slate-300">Rubric:</strong> Full credit (5 pts): Clear explanation of both concepts with examples. Partial credit (3 pts): Mentions key difference but lacks detail. No credit (0 pts): Incorrect or missing explanation.</p>
                    </div>
                    <button
                      onClick={() => loadExample(2)}
                      className="text-sm px-4 py-2 bg-violet-600/20 hover:bg-violet-600/30 text-violet-300 rounded-lg border border-violet-500/30 transition-all"
                    >
                      📋 Use Example 2
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        
        * {
          font-family: 'DM Sans', system-ui, -apple-system, sans-serif;
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 0.4;
          }
          50% {
            opacity: 0.6;
          }
        }

        .animate-pulse {
          animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        .delay-1000 {
          animation-delay: 1s;
        }

        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slide-in-from-top-2 {
          from {
            transform: translateY(-0.5rem);
          }
          to {
            transform: translateY(0);
          }
        }

        .animate-in {
          animation: fade-in 0.3s ease-out, slide-in-from-top-2 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default AutoGrader;
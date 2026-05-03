import { useState, useRef } from 'react';

function App() {
  const [state, setState] = useState('idle'); 
  // states: idle, knocking, dylan_speaking, ready_to_record, recording, loading, result
  const [resultData, setResultData] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const playKnock = () => {
    setState('knocking');
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendAudioToBackend(audioBlob);
      };

      mediaRecorderRef.current.start();
      setState('recording');
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Microphone access is required to use this app.");
      setState('ready_to_record');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setState('loading');
    }
  };

  const sendAudioToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.webm");

    try {
      const response = await fetch("http://localhost:8000/api/v1/knock", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Server responded with an error");
      }

      const data = await response.json();
      setResultData(data);
      setState('result');
    } catch (err) {
      console.error("Backend error:", err);
      alert("An error occurred while communicating with the server.");
      setState('ready_to_record');
    }
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-white font-serif flex items-center justify-center relative overflow-hidden" style={{ fontFamily: "'Playfair Display', serif" }}>
      
      {/* Background Image */}
      <img
        src={state === 'result' && resultData ? `http://localhost:8000${resultData.image_url}` : '/assets/intro-bg.jpg'}
        className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-3000 ease-in-out ${state === 'result' ? 'opacity-40' : 'opacity-20'}`}
        alt="Background"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-900/70 to-transparent" />

      {/* State Renderers */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full h-full px-6 text-center">
        
        {state === 'idle' && (
          <div className="animate-fade-in-up max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto bg-black/60 rounded-lg p-4 backdrop-blur-sm text-center">
            <h1 className="text-5xl md:text-7xl mb-16 opacity-90 font-bold tracking-widest drop-shadow-xl text-white">The Dylan Door</h1>
              <button 
                onClick={playKnock}
                className="w-56 h-56 rounded-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 border-4 border-white hover:shadow-2xl hover:scale-105 transition-all duration-500 ease-out flex items-center justify-center text-3xl font-bold tracking-widest text-white shadow-[0_0_40px_rgba(255,255,255,0.7)]"
              >
                KNOCK
              </button>
            <p className="mt-8 text-neutral-500 italic tracking-widest">Click to approach</p>
          </div>
        )}

        {state === 'knocking' && (
          <div className="animate-pulse max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto bg-black/60 rounded-lg p-4 backdrop-blur-sm text-center">
            <h2 className="text-2xl text-white italic tracking-widest drop-shadow-md">Knocking on the door...</h2>
            <audio 
              autoPlay 
              src="/assets/knock.mp3" 
              onEnded={() => setState('dylan_speaking')} 
            />
          </div>
        )}

        {state === 'dylan_speaking' && (
          <div className="animate-fade-in-up max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto bg-black/60 rounded-lg p-4 backdrop-blur-sm text-center">
            <h2 className="text-2xl text-white italic tracking-widest drop-shadow-md">Listening to the voice inside...</h2>
            <audio 
              autoPlay 
              src="/assets/dylan-intro.mp3" 
              onEnded={() => setState('ready_to_record')} 
            />
          </div>
        )}

        {state === 'ready_to_record' && (
          <div className="animate-fade-in-up">
            <p className="mb-12 text-2xl md:text-3xl text-neutral-300 italic tracking-wider">It's your turn to speak.</p>
              <button 
                onClick={startRecording}
                className="w-56 h-56 rounded-full bg-gradient-to-r from-red-600 via-pink-600 to-purple-600 border-4 border-white hover:shadow-2xl hover:scale-105 transition-all duration-500 ease-out flex items-center justify-center text-3xl font-bold tracking-widest text-white shadow-[0_0_40px_rgba(255,0,0,0.8)]"
              >
                RECORD
            </button>
            <p className="mt-8 text-neutral-500 italic tracking-widest">Click to start recording</p>
          </div>
        )}

        {state === 'recording' && (
          <div className="flex flex-col items-center">
                <button 
                  onClick={stopRecording}
                  className="w-56 h-56 rounded-full bg-gradient-to-r from-red-700 via-pink-700 to-purple-700 border-4 border-white hover:shadow-2xl hover:scale-105 transition-all duration-500 ease-out flex items-center justify-center text-3xl font-bold tracking-widest text-white shadow-[0_0_40px_rgba(255,0,0,0.8)]"
                >
                  STOP
            </button>
            <div className="mt-12 flex space-x-3 items-center">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
              <p className="text-red-400 italic tracking-widest">Recording...</p>
            </div>
            <p className="mt-6 text-neutral-500 italic">Pour your heart out, then click STOP.</p>
          </div>
        )}

        {state === 'loading' && (
          <div className="flex flex-col items-center">
            <div className="text-3xl md:text-5xl animate-pulse text-neutral-400 font-bold tracking-widest drop-shadow-xl">
              Waiting for an answer...
            </div>
            <p className="mt-8 text-neutral-600 italic tracking-widest">The door is slowly opening</p>
          </div>
        )}

        {state === 'result' && resultData && (
          <div className="flex flex-col items-center justify-end w-full h-full pb-20 max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto bg-black/60 rounded-lg p-6 backdrop-blur-sm text-center">
            <p className="text-neutral-400 mb-16 italic opacity-70 text-xl max-w-2xl px-4 drop-shadow-md">
              "{resultData.text_transcribed}"
            </p>
            
            <div className="space-y-8 text-3xl md:text-5xl leading-relaxed max-w-5xl font-bold drop-shadow-[0_5px_5px_rgba(0,0,0,1)] px-4">
                {resultData.poem.split('\n').filter(line => line.trim() !== '').map((line, idx) => (
                  <p key={idx} className="animate-fade-in-up text-2xl md:text-3xl font-medium text-white drop-shadow-md" style={{ animationDelay: `${idx * 2}s` }}>
                    {line}
                  </p>
                ))}
            </div>
            
            <button 
              onClick={() => { setState('idle'); setResultData(null); }}
              className="mt-24 px-10 py-4 border border-neutral-600 rounded-full text-neutral-400 hover:text-white hover:border-white hover:bg-white/5 transition-all duration-500 tracking-widest uppercase text-sm"
            >
              Knock Again
            </button>

            {/* Sesi otomatik oynat */}
            <audio src={`http://localhost:8000${resultData.audio_url}`} autoPlay />
          </div>
        )}

      </div>
    </div>
  );
}

export default App;

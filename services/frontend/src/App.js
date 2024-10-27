import React, { useState, useEffect, useRef } from 'react';
import Handlebars from 'handlebars';

function App() {
  const [template, setTemplate] = useState('');
  const [htmlContent, setHtmlContent] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const intervalRef = useRef(null);

  const sampleLength = 10 * 1000;
  const sampleInterval = 12 * 1000;

  useEffect(() => {
    fetch('/template.html')
      .then(response => response.text())
      .then(text => setTemplate(text))
      .catch(error => {
        console.error('TuneCube: Template error:', error);
      });
  }, []);

  useEffect(() => {
    let stream;

    const startRecording = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.ondataavailable = event => {
          audioChunksRef.current.push(event.data);
        };

        mediaRecorderRef.current.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          audioChunksRef.current = [];

          const formData = new FormData();
          formData.append('audio', audioBlob, 'sample.webm');

          try {
            const response = await fetch('/detect', {
              method: 'POST',
              body: formData,
            });

            const data = await response.json();

            if (template) {
              const compiledTemplate = Handlebars.compile(template);
              const renderedHtml = compiledTemplate({ results: data });
              setHtmlContent(renderedHtml);
            }
          } catch (error) {
            console.error('TuneCube: Data error:', error);
          }
        };

        recordSample();

        intervalRef.current = setInterval(recordSample, sampleInterval);
      } catch (error) {
        console.error('TuneCube: Microphone access error:', error);
      }
    };

    const recordSample = () => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'inactive') {
        mediaRecorderRef.current.start();

        setTimeout(() => {
          mediaRecorderRef.current.stop();
        }, sampleLength);
      }
    };

    if (template) {
      startRecording();
    }

    return () => {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
      clearInterval(intervalRef.current);
    };
  }, [template]);

  return (
    <div id="app">
      <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
    </div>
  );
}

export default App;
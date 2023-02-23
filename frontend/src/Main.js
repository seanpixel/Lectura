import React, { useState } from "react";
import axios from "axios";

const Main = () => {
  const [file, setFile] = useState(null);
  const [studyGuide, setStudyGuide] = useState({});

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };
  const uploadMp3 = async () => {
    // event.preventDefault();

    return new Promise((resolve, reject) => {
      const mp3Data = new FormData();
      mp3Data.append("mp3", file);

      axios
        .post("http://localhost:3200/upload", mp3Data) //could be post or get
        .then((response) => {
          console.log("MP3 uploaded successfully");
          console.log(response.data);
          setStudyGuide(response.data); //may be response.data.text
        })
        .catch((error) => {
          console.error("Error uploading MP3");
          console.error(error);
          reject("error uploading MP3");
        });
    });
  };
  const handleSubmit = async () => {
    const output = await uploadMp3;
    console.log(output);
  };
  return (
    <>
      <h1>Stutora</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Choose an mp3 to upload:
          <input
            accept=".mp3,audio/*"
            type="file"
            name="mp3"
            onChange={handleFileUpload}
          />
          <input type="submit" />
        </label>
      </form>
      <div>
        {studyGuide.length>0 && (
          <>
            <p>{studyGuide.summary}</p>
            {studyGuide.keyTerms.map((element, index) => {
              <div id={index}>
                <p>
                  {element.term}: {element.definition}
                </p>
              </div>;
            })}
          </>
        )}
      </div>
    </>
  );
};
export default Main;

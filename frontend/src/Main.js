import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const Main = () => {
  const object = {
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    keyterms: [
      { term: "Term1", definition: "Definition1" },
      { term: "Term2", definition: "Definition2" },
      { term: "Term3", definition: "Definition3" },
    ],
  };
  const [file, setFile] = useState(null);
  const [studyGuide, setStudyGuide] = useState(object);

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
      <h1 className=" text-6xl font-bold leading-snug mt-0 mb-2 text-teal-800 mb-0">
        Lectura
      </h1>
      <p className="font-bold text-teal-700 mt-0">Generate a study guide from your lecture recording!</p>
      <form className="my-5 mx-auto flex flex-col w-4/5" onSubmit={handleSubmit}>
        <StyledFileSelect
          accept=".mp3,audio/*"
          type="file"
          name="mp3"
          onChange={handleFileUpload}
          className="text-gray-400 font-bold"
        />
        <input
          className="my-5 bg-teal-600 hover:bg-teal-800 text-white font-bold py-2 px-4 rounded w-1/6"
          type="submit"
          value="Generate"
        />
      </form>
      <div className="mx-auto w-4/5">
        {studyGuide && (
          <>
            <p className="font-mono py-7 text-left">{studyGuide.summary}</p>
            {studyGuide.keyterms.map((element, index) => (
              <div id={index}>
                <p className="font-mono text-left">
                  <span className="font-mono font-bold pr-5">{element.term}:</span>{" "}
                  {element.definition}
                </p>
              </div>
            ))}
          </>
        )}
      </div>
    </>
  );
};
const StyledFileSelect = styled.input`
border: 1px solid #00695C;
border-radius:5px;
width: 30%;
  ::file-selector-button {
    font-weight: bold;
    color: white;
    background: #00695C;
    padding: 0.5em;
    border: none;
  }
`;
export default Main;

import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";
import BarLoader from "react-spinners/BarLoader";
import { usePromiseTracker, trackPromise } from "react-promise-tracker";

const Main = () => {
  // const object = {
  //   summary:
  //     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  //   keyterms: [
  //     { term: "Term1", definition: "Definition1" },
  //     { term: "Term2", definition: "Definition2" },
  //     { term: "Term3", definition: "Definition3" },
  //   ],
  // };
  const { promiseInProgress } = usePromiseTracker();

  const [file, setFile] = useState(null);
  const [studyGuide, setStudyGuide] = useState(null);
  const [question, setQuestion] = useState("");
  const [questionResponse, setQuestionResponse] = useState("");
  const [link, setLink] = useState("");

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const uploadMp3 = async () => {
    // event.preventDefault();

    return new Promise((resolve, reject) => {
      const mp3Data = new FormData();
      mp3Data.append("mp3", file);

      // const reader = new FileReader();
      // reader.readAsBinaryString(file);
      trackPromise(
        axios
          .post("http://127.0.0.1:5000/audio", mp3Data)
          .then((response) => {
            console.log("MP3 uploaded successfully");
            console.log(response.data);
            setStudyGuide(response.data); //may be response.data.text
            resolve("success");
          })
          .catch((error) => {
            console.error("Error uploading MP3");
            console.error(error);
            reject("error uploading MP3");
          })
      );
    });
  };
  const getMp3 = async () => {
    return new Promise((resolve, reject) => {

      trackPromise(
        axios
          .post("http://127.0.0.1:5000/convert", {link: link})
          .then((response) => {
            console.log("MP3 uploaded successfully");
            console.log(response.data);
            setStudyGuide(response.data); //may be response.data.text
            resolve("success");
          })
          .catch((error) => {
            console.error("Error retreiving youtube video");
            console.error(error);
            reject("error uploading MP3");
          })
      );
    });
  };
  const askQuestion = async () => {
    axios
      .get("http://127.0.0.1:5000/question", question) //could be post or get
      .then((response) => {
        console.log("Question uploaded successfully");
        console.log(response.data.answer);
        setQuestionResponse(response.data.answer);
      })
      .catch((error) => {
        console.error("Error retreiving question");
        console.error(error);
      });
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      const output = await uploadMp3();
      console.log(output)
    } else if (link) {
      const output = await getMp3();
      console.log(output)
    }
  };
  const handleQuestion = async () => {
    const output = await askQuestion();
    console.log(output);
  };
  return (
    <div className="dark:bg-black">
      <h1 className="text-6xl font-bold leading-snug mt-0 mb-2 text-teal-800 mb-0">
        Lectura
      </h1>
      <p className="font-bold text-lg text-teal-700 mt-0">
        Generate a study guide from your lecture recording!
      </p>
      <form
        className="my-5 mx-auto flex flex-col w-4/5"
        onSubmit={handleSubmit}
      >
        <label className="font-bold text-lg text-left text-teal-700  mb-4">
          Upload an MP3 Lecture Recording
        </label>
        <div className="flex w-1/2">
          <StyledFileSelect
            accept=".mp3,audio/*"
            type="file"
            name="mp3"
            onChange={handleFileUpload}
            className="text-gray-400 font-bold"
          />
          <p className="px-3 text-3xl text-teal-800">/</p>
          <input
            onChange={(event) => setLink(event.target.value)}
            className="pl-3 text-gray-400 font-bold border w-52 "
            placeholder="paste a youtube link"
          ></input>
        </div>

        <input
          className="my-5 bg-teal-600 hover:bg-teal-800 text-white font-bold py-2 px-4 rounded w-1/6"
          type="submit"
          value="Generate"
        />
      </form>
      <div className="mx-auto w-4/5">
        {promiseInProgress && <BarLoader color="#00695c"></BarLoader>}
        {studyGuide && (
          <>
            <p className="font-mono py-7 text-left">{studyGuide.summary}</p>
            <p className="font-mono py-7 text-left">
              {studyGuide.transcription}
            </p>
            {/* {studyGuide.keyterms.map((element, index) => (
              <div id={index}>
                <p className="font-mono text-left">
                  <span className="font-mono font-bold pr-5">
                    {element.term}:
                  </span>{" "}
                  {element.definition}
                </p>
              </div>
            ))} */}
          </>
        )}
      </div>
      <form
        className="my-5 mx-auto flex flex-col w-4/5"
        onSubmit={handleQuestion}
      >
        {/* <label class="text-left ">Ask a question !</label> */}
        <input
          accept=".mp3,audio/*"
          type="text"
          name="question"
          onChange={(event) => setQuestion(event.target.value)}
          className="text-gray-400 font-bold border w-1/5 p-3"
          placeholder="Ask me a question !"
        />
        <input
          className="my-5 bg-teal-600 hover:bg-teal-800 text-white font-bold py-2 px-4 rounded w-1/6"
          type="submit"
          value="Generate"
        />
      </form>
    </div>
  );
};
const StyledFileSelect = styled.input`
  border: 1px solid #00695c;
  border-radius: 5px;
  width: 200px;
  ::file-selector-button {
    font-weight: bold;
    color: white;
    background: #00695c;
    padding: 0.5em;
    border: none;
  }
`;
export default Main;

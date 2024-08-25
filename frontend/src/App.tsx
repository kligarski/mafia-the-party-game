import useWebSocket from "react-use-websocket";
import "./App.css";
import { useEffect, useState } from "react";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-json"
import "ace-builds/src-noconflict/theme-github_dark"
import "ace-builds/src-noconflict/ext-language_tools";

function App() {
  const gameCode = JSON.parse(
    String(document.getElementById("game-code")?.textContent)
  );
  const socketUrl = "ws://127.0.0.1:8000/ws/game/" + gameCode + "/";

  const [wsMsg, setWsMsg] = useState<string>("{\n  \"action\": \n  \"data\": \n}");

  const [messages, setMessages] = useState<any[]>([]);

  const { sendMessage, lastMessage, lastJsonMessage } = useWebSocket<any>(socketUrl, {
    onOpen: () => console.log("opened ws connection"), // development-only
    shouldReconnect: (_) => true, // development-only
  });

  useEffect(() => {
    if (lastMessage != null) {
      console.log(lastJsonMessage);
      setMessages([lastJsonMessage, ...messages])
    }
  }, [lastMessage]);

  interface FormElements extends HTMLFormControlsCollection {
    wsMsg: HTMLInputElement;
  }
  interface MessageFromElement extends HTMLFormElement {
    readonly elements: FormElements;
  }

  function sendEvent(e: React.FormEvent<MessageFromElement>) {
    e.preventDefault();
    console.log(wsMsg);
    sendMessage(wsMsg);
  }

  return (
    <>
      <h1>Game: {gameCode}</h1>
      <h2>Send WS event:</h2>
      <form onSubmit={sendEvent} style={{display: "flex", alignItems: "center", flexDirection:"column"}}>
        <AceEditor 
          mode="json"
          theme="github_dark"
          name="wsMsg"
          editorProps={{ $blockScrolling: true }}
          value={wsMsg}
          onChange={(value) => {
            setWsMsg(value);
          }}
          height="300px"
          />
        <button type="submit">Send</button>
      </form>
      <h2>Last messages:</h2>
      {messages.map(msg => <textarea rows={15} cols={80} readOnly={true} value={JSON.stringify(msg, null, 2)}/>)}
      
    </>
  );
}

export default App;

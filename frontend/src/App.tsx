import useWebSocket from "react-use-websocket";
import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const gameCode = JSON.parse(
    String(document.getElementById("game-code")?.textContent)
  );
  const socketUrl = "ws://127.0.0.1:8000/ws/game/" + gameCode + "/";

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
    const msg = e.currentTarget.elements.wsMsg.value ? e.currentTarget.elements.wsMsg.value : "";

    sendMessage(msg);
  }

  return (
    <>
      <h1>Game: {gameCode}</h1>
      <h2>Send WS event:</h2>
      <form onSubmit={sendEvent}>
        <textarea rows={15} cols={80} name="wsMsg" id="wsMsg" defaultValue={"{\n\n}"} /><br/>
        <button type="submit">Send</button>
      </form>
      <h2>Last messages:</h2>
      {messages.map(msg => <textarea rows={15} cols={80} readOnly={true} value={JSON.stringify(msg, null, 2)}/>)}
      
    </>
  );
}

export default App;

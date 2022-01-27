import React from "react";
import { observeAccountChanges } from "./webSocket/webSocket";
import "./App.css";

export const App: React.FC = () => {
  const [observedChange, setObservedChange] = React.useState<number>();
  observeAccountChanges({ callbackFunction: setObservedChange });

  return <div className="App">latest balance change to: {<p>{observedChange}</p>}</div>;
};

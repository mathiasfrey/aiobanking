export const getInitialAccountData = () => {};

export const observeAccountChanges: () => void = () => {
  const accountChangesWS = new WebSocket("ws://127.0.0.1:8003/ws-raw");
  accountChangesWS.onopen = () => {
    console.log("connected");
  };
  accountChangesWS.onmessage = (evt) => {
    const message = JSON.parse(evt.data);
    console.log(message);
  };
  const closeConnection = () => {
    accountChangesWS.onclose = () => {
      console.log("disconnected");
      // automatically try to reconnect on connection loss
    };
  };
};

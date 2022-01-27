import React from "react";
import { Container, Table } from "react-bootstrap";
import { getAccounts } from "./api/getAccounts";
import "./App.css";
import { Account } from "./components/Account/Account";
export interface AccountDataInterface {
  id: number;
  account: string;
  balance: number;
  modeloutput?: number;
}

export const App: React.FC = () => {
  const singleAccountRawUpdateAdressWS = "ws://127.0.0.1:8003/ws-raw";
  const singleAccountProcessedUpdateAdressWS = "ws://127.0.0.1:8003/ws";
  const rawSingleAccountUpdateWS = new WebSocket(singleAccountRawUpdateAdressWS);
  const processedSingleAccountUpdateWS = new WebSocket(singleAccountProcessedUpdateAdressWS);

  const [accountData, setAccountData] = React.useState<AccountDataInterface[]>([]);
  const [rawAccountUpdate, setRawAccountUpdate] = React.useState<AccountDataInterface>();
  const [processedAccountUpdate, setProcessedAccountUpdate] = React.useState<AccountDataInterface>();

  //Fetches initial accounts; Listens to websockets for account raw-data updates and proccessed-data updates
  React.useEffect(() => {
    getAccounts()
      .then((data) => {
        setAccountData(data);
      })
      .catch(({ message }) => {
        console.log("Loading accounts has failed");
      });

    rawSingleAccountUpdateWS.onopen = () => {
      console.log(`Connected: ${singleAccountRawUpdateAdressWS}`);
    };
    rawSingleAccountUpdateWS.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      message.payload && setRawAccountUpdate(message.payload.after);
    };
    processedSingleAccountUpdateWS.onopen = () => {
      console.log(`Connected: ${singleAccountProcessedUpdateAdressWS}`);
    };
    processedSingleAccountUpdateWS.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      setProcessedAccountUpdate(message);
    };
  }, []);

  //Propagates account raw-data updates to the state
  React.useEffect(() => {
    const newState = [...accountData];
    newState.forEach((account) => {
      if (account.id === rawAccountUpdate?.id) {
        account.balance = rawAccountUpdate?.balance;
      }
    });
    setAccountData(newState);
  }, [rawAccountUpdate]);

  //Propagates account processed-data updates to the state
  React.useEffect(() => {
    const newState = [...accountData];
    newState.forEach((account) => {
      if (account.account === processedAccountUpdate?.account) {
        account.modeloutput = processedAccountUpdate?.modeloutput;
      }
    });
    setAccountData(newState);
  }, [processedAccountUpdate]);

  return (
    <Container fluid="sm" className="App my-4">
      <Table striped bordered hover size="sm">
        <thead>
          <tr>
            <th>#</th>
            <th className="text-start">Account</th>
            <th>Balance</th>
            <th>Model Output</th>
          </tr>
        </thead>
        <tbody>
          {accountData.map((item) => (
            <Account key={item.id} id={item.id} account={item.account} balance={item.balance} modeloutput={item.modeloutput} />
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

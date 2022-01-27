import React from "react";
import { AccountDataInterface } from "../../App";
export const Account: React.FC<AccountDataInterface> = ({ id, account, balance, modeloutput }) => {
  return (
    <tr>
      <td>{id}</td>
      <td className="text-start">{account}</td>
      <td>{balance}</td>
      <td>{modeloutput}</td>
    </tr>
  );
};

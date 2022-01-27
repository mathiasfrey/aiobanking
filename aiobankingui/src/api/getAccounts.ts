export async function getAccounts() {
  const response = await fetch("http://127.0.0.1:8003/table");
  const accounts = await response.json();
  if (response.ok === true) {
    return accounts;
  } else {
    console.log(response.status, response.statusText);
  }
}

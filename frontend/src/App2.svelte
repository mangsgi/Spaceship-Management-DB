.mechanic-page {
  text-align: center;
  padding: 50px;
}
.mechanic-page button {
  margin: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1em;
}
.button-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  font-size: 1em;
  margin: 5px;
}

.button-link:hover {
  background-color: #0056b3;
}
.error {
  color: red;
}
.loading {
  font-style: italic;
}
table {
  margin: 20px auto;
  border-collapse: collapse;
  width: 90%;
}
th, td {
  border: 1px solid #ddd;
  padding: 12px;
}
th {
  background-color: #f2f2f2;
}
form {
  margin: 20px auto;
  width: 90%;
  max-width: 600px;
  text-align: left;
}
form input, form textarea {
  width: 100%;
  padding: 8px;
  margin: 5px 0 15px 0;
  box-sizing: border-box;
}
form button {
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1em;
}

.records-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-top: 40px;
}

.records-section > div {
  width: 45%;
  min-width: 300px;
}

@media (max-width: 800px) {
  .records-section {
    flex-direction: column;
    align-items: center;
  }
  .records-section > div {
    width: 90%;
  }
}
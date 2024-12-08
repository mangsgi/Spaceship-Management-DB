<!-- src/routes/mechanic/page.svelte -->
<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { navigate } from "svelte-routing"; // Ensure this is appropriate for your setup
  import { userId } from "../../../stores.js"; // Adjust the path as needed
  import axios from "axios";

  // Loading and error states
  const loading = writable(false);
  let errorMessage = "";
  let errorMessage_get = "";
  let errorMessage_records = "";

  $: adminId = $userId;

  // Variables for pilot and flight assignment
  let pilot_id = "";
  let flight_id = "";

  // No-assigned flights
  let no_assign_flights = [];

  // Available spaceships
  let available_spaceships = [];

  // Navigate to home
  function navigateHome() {
    navigate("/");
  }

  // 조종사 비행 할당 (Assign Pilot to Flight)
  async function CombinePilotFlight(event) {
    event.preventDefault();
    loading.set(true);
    errorMessage = "";

    const endpoint = "http://localhost:8000/pilot_flights/pilot_assignment/";

    const payload = {
      pilot_id: parseInt(pilot_id),
      flight_id: parseInt(flight_id),
    };

    try {
      const response = await axios.post(endpoint, payload);
      if (response.data) {
        console.log("추가된 기록:", response.data);
        // 입력 필드 초기화
        pilot_id = "";
        flight_id = "";
        // 유지보수 작업 목록 갱신
        findFlightsNoPilot();
      } else {
        errorMessage = "유지보수 기록을 추가할 수 없습니다.";
      }
    } catch (error) {
      console.error("데이터를 추가하는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = "잘못된 요청입니다. 입력 데이터를 확인해주세요.";
        } else if (error.response.status === 422) {
          errorMessage =
            "서버가 요청을 이해했으나 처리할 수 없습니다. 요청 데이터를 확인해주세요.";
        } else if (error.response.status === 404) {
          errorMessage = "해당 작업을 찾을 수 없습니다.";
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  // Fetch flights without assigned pilots
  async function findFlightsNoPilot() {
    loading.set(true);
    errorMessage_records = "";

    const endpoint_get = "http://localhost:8000/flights_unassigned";

    try {
      const response = await axios.get(endpoint_get);
      if (Array.isArray(response.data)) {
        const matchedItems = response.data;
        console.log("Unassigned flights:", matchedItems);
        if (matchedItems.length > 0) {
          no_assign_flights = matchedItems;
          console.log("Unassigned flights:", no_assign_flights);
        } else {
          errorMessage_records = "할당되지 않은 비행을 찾을 수 없습니다.";
        }
      } else {
        errorMessage_records = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error("데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_records = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
        } else {
          errorMessage_records = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_records = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  // Fetch available spaceships
  async function findSpaceshipAdmin() {
    loading.set(true);
    errorMessage_get = "";

    const endpoint_spaceships = "http://localhost:8000/available_spaceships"; // Adjust the endpoint as needed

    try {
      const response = await axios.get(endpoint_spaceships);
      if (Array.isArray(response.data)) {
        available_spaceships = response.data;
        console.log("Available spaceships:", available_spaceships);
      } else {
        errorMessage_get = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error(
        "Available spaceships 데이터를 가져오는 중 오류 발생:",
        error,
      );
      if (error.response) {
        errorMessage_get = `서버 오류 발생: ${error.response.status}`;
      } else {
        errorMessage_get = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    findFlightsNoPilot(); // Optionally fetch unassigned flights on mount
  });
</script>

<div class="admin-page">
  <div class="admin-container">
    <h1>Add Pilot for Flights</h1>
    <p>Admin ID: {adminId}</p>
    <button on:click={() => navigate("/admin")}>Back to Menu </button>

    {#if $loading}
      <p class="loading">Loading...</p>
    {/if}

    <div class="record-section">
      <!-- Flight Creation -->

      <!-- Unassigned Flights List -->
      <div>
        {#if no_assign_flights.length > 0}
          <h3>Non Assginment Flights</h3>
          <table>
            <thead>
              <tr>
                <th>Flight ID</th>
                <th>Spaceship ID</th>
                <th>Departure Location</th>
                <th>Arrival Location</th>
                <th>Departure Time</th>
                <th>Arrival Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {#each no_assign_flights as flight}
                <tr>
                  <td>{flight.flight_id}</td>
                  <td>{flight.spaceship_id}</td>
                  <td>{flight.departure_location}</td>
                  <td>{flight.arrival_location}</td>
                  <td
                    >{flight.departure_time
                      ? new Date(flight.departure_time).toLocaleString()
                      : "-"}</td
                  >
                  <td
                    >{flight.arrival_time
                      ? new Date(flight.arrival_time).toLocaleString()
                      : "-"}</td
                  >
                  <td>{flight.status}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {:else if !errorMessage_records && !$loading}
          <p>There is no one non-assgined flight!</p>
        {/if}
      </div>
    </div>

    <!-- 할당하기 (Assign Pilot to Flight) -->
    <div>
      <h2>Add Pilot</h2>
      {#if errorMessage}
        <p class="error">{errorMessage}</p>
      {/if}
      <form on:submit={CombinePilotFlight}>
        <label for="pilot_id">Pilot ID:</label>
        <input
          type="number"
          id="pilot_id"
          bind:value={pilot_id}
          placeholder="Pilot ID"
          required
        />

        <label for="flight_id">Flight ID:</label>
        <input
          type="number"
          id="flight_id"
          bind:value={flight_id}
          placeholder="Flight ID"
          required
        />

        <button type="submit">Add</button>
      </form>
    </div>
  </div>
</div>
<!-- 
<style>
  .mechanic-page,
  .admin-page {
    text-align: center;
    padding: 50px;
  }
  .mechanic-page button,
  .admin-page button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  .button-link {
    display: inline-block;
    padding: 10px 20px;
    background-color: #007bff;
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
  th,
  td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: center;
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
  form input,
  form textarea {
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
</style> -->


<style>
  @import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap");

  .admin-page {
  position: absolute; /* 또는 fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  text-align: center;
  padding: 0; /* 패딩 제거 */
  background-image: url('/images/space_main.png'); /* 원하는 배경 이미지 경로 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
  background-attachment: fixed; /* 배경 이미지 고정 */
  color: white;
  width: 100vw; /* 전체 뷰포트 너비의 120% */
  height: 120vh; /* 전체 뷰포트 높이의 120% */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Orbitron', sans-serif;
  overflow: hidden; /* 필요에 따라 추가 */
}

.admin-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
    max-height: 80vh; /* 컨테이너 최대 높이 지정 */
    overflow: auto;   /* 컨테이너 내부 내용이 많을 경우 스크롤 발생 */
}

  h1,
  h2,
  h3 {
    font-family: "Orbitron", sans-serif;
  }

  h1 {
    font-size: 3em;
    margin-bottom: 20px;
  }

  h2 {
    font-size: 2em;
    margin-bottom: 20px;
  }

  h3 {
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  label {
    width: 100%;
    margin: 10px 0;
    text-align: left;
    font-size: 1em;
  }

  input[type="text"],
  input[type="date"],
  input[type="file"] {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 2px solid white;
    border-radius: 10px;
    background-color: transparent;
    color: white;
    font-family: "Orbitron", sans-serif;
    font-size: 1em;
  }

  input::placeholder {
    color: #ccc;
  }

  button {
    font-family: "Orbitron", sans-serif;
    font-size: 1em;
    margin: 10px 0;
    padding: 10px 20px;
    border-radius: 50px;
    border: 2px solid white;
    background-color: transparent;
    color: white;
    transition:
      background-color 0.3s,
      color 0.3s;
    width: 100%;
    cursor: pointer;
  }

  button:hover {
    background-color: white;
    color: black;
  }

  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 100%;
    color: white;
  }

  th,
  td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }

  th {
    background: #333;
  }

  tbody {
    background-color: rgba(0, 0, 0, 0.5); /* White with 80% opacity */
  }

  .loading {
    font-style: italic;
    margin-top: 10px;
  }

  .error {
    color: #ffcccc;
    font-size: 1em;
    margin-top: 10px;
  }

  .home-button {
    width: auto;
    margin: 10px 0;
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
</style>

<!-- src/routes/mechanic/page.svelte -->
<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { navigate } from 'svelte-routing'; // Ensure this is appropriate for your setup
  import { userId } from '../../../stores.js'; // Adjust the path as needed
  import axios from 'axios';

  // Loading and error states
  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';
  let errorMessage_records = '';

  $: adminId = $userId;

  // Flight addition fields
  let departure_location = '';
  let arrival_location = '';
  let departure_time = '';
  let arrival_time = '';
  let flight_status = '';
  let spaceship_id = ''; // To be selected from available spaceships

  // No-assigned flights
  let no_assign_flights = [];

  // Available spaceships
  let select_departure_time = null;
  let select_arrival_time = null;
  let available_spaceships = [];

  // Navigate to home
  function navigateHome() {
    navigate('/');
  }

  // Fetch available spaceships (추가구현 : 현재 우주선의 마지막 위치 : 비행 일정 조회 by 고객으로 마지막 arrival_location 불러오기)
  async function findSpaceshipAdmin() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_get = 'http://localhost:8000/spaceships/available';

    try {
      const response = await axios.get(endpoint_get, {
        params: { 
          departure_time: select_departure_time,
          arrival_time: select_arrival_time,
        }
      });
      if (Array.isArray(response.data)) {
        const matchedItems = response.data;
        console.log('Available spaceships:', matchedItems);
        if (matchedItems.length > 0) {
          available_spaceships = matchedItems;
          console.log('Available spaceships:', available_spaceships);
        } else {
          errorMessage_get = '해당 우주선을 찾을 수 없습니다.';
        }
      } else {
        errorMessage_get = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  // Add a new flight
  async function addFlights(event) {
    event.preventDefault();
    loading.set(true);
    errorMessage = '';

    const endpoint = 'http://localhost:8000/flights';

    const payload = {
      spaceship_id: spaceship_id, // Use the selected spaceship_id
      departure_location: departure_location,
      arrival_location: arrival_location,
      departure_time: departure_time,
      arrival_time: arrival_time,
      status: flight_status
    };

    try {
      const response = await axios.post(endpoint, payload);
      if (response.data) {
        console.log('추가된 기록:', response.data);
        // Reset input fields
        spaceship_id = '';
        departure_location = '';
        arrival_location = '';
        departure_time = '';
        arrival_time = '';
        flight_status = '';
        // Optionally, refresh the available spaceships or fetch unassigned flights
        findFlightsNoPilot();
      } else {
        errorMessage = '비행을 생성할 수 없습니다.';
      }
    } catch (error) {
      console.error('데이터를 추가하는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 데이터를 확인해주세요.';
        } else if (error.response.status === 422) {
          errorMessage = '서버가 요청을 이해했으나 처리할 수 없습니다. 요청 데이터를 확인해주세요.';
        } else if (error.response.status === 404) {
          errorMessage = '해당 작업을 찾을 수 없습니다.';
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  // Fetch flights without assigned pilots
  async function findFlightsNoPilot() {
    loading.set(true);
    errorMessage_records = '';

    const endpoint_get = 'http://localhost:8000/flights_unassigned';

    try {
      const response = await axios.get(endpoint_get);
      if (Array.isArray(response.data)) {
        const matchedItems = response.data;
        console.log('Unassigned flights:', matchedItems);
        if (matchedItems.length > 0) {
          no_assign_flights = matchedItems;
          console.log('Unassigned flights:', no_assign_flights);
        } else {
          errorMessage_records = '할당되지 않은 비행을 찾을 수 없습니다.';
        }
      } else {
        errorMessage_records = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_records = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_records = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_records = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    findSpaceshipAdmin();
  });
</script>

<!-- <style>
  .mechanic-page, .admin-page {
    text-align: center;
    padding: 50px;
  }
  .mechanic-page button, .admin-page button {
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
    width: 85%;
    max-width: 1500px;
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


<div class="admin-page">
<div class="admin-container">
  <h1>Add Flights & Tasks</h1>
  <p>Admin ID: {adminId}</p>
  <button on:click={() => navigate("/admin")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  <!-- Available Spaceships -->
  {#if available_spaceships.length > 0}
    <h2>Flightable Spaceship List</h2>
    <table>
      <thead>
        <tr>
          <th>Spaceship ID</th>
          <th>Model Name</th>
          <th>Manufacture Date</th>
          <th>Last Maintenance Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {#each available_spaceships as spaceship}
          <tr>
            <td>{spaceship.spaceship_id}</td>
            <td>{spaceship.model}</td>
            <td>{new Date(spaceship.manufacture_date).toLocaleDateString()}</td>
            <td>{new Date(spaceship.last_maintenance_date).toLocaleDateString()}</td>
            <td>{spaceship.status}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else if !errorMessage_get && !$loading}
    <p>There is no available spaceship.</p>
  {/if}

  <div class="records-section">
    <!-- Flight Creation -->
    <div>
      <h2>Add Flight</h2>
      {#if errorMessage}
        <p class="error">{errorMessage}</p>
      {/if}
      <form on:submit={addFlights}>
        <label for="spaceship_id">Spaceship ID:</label>
        <input type="number" id="spaceship_id" bind:value={spaceship_id} placeholder="Spaceship ID" required />

        <label for="departure_location">Departure Location:</label>
        <input type="text" id="departure_location" bind:value={departure_location} placeholder="Departure Location" required />

        <label for="arrival_location">Arrival Location:</label>
        <input type="text" id="arrival_location" bind:value={arrival_location} placeholder="Arrival Location" required />

        <label for="departure_time">Departure Time:</label>
        <input type="datetime-local" id="departure_time" bind:value={departure_time} required />

        <label for="arrival_time">Arrival Time:</label>
        <input type="datetime-local" id="arrival_time" bind:value={arrival_time} required />

        <label for="flight_status">Flight Status:</label>
        <input type="text" id="flight_status" bind:value={flight_status} placeholder="Flight Status" required />

        <button type="submit">Add</button>
      </form>
    </div>

    <!-- Unassigned Flights List -->
    <div>
      <h2>No Assignment Flight</h2>
      {#if errorMessage_records}
        <p class="error">{errorMessage_records}</p>
      {/if}
      <form on:submit|preventDefault={findFlightsNoPilot}>
        <button type="submit">Search Flights</button>
      </form>

      {#if no_assign_flights.length > 0}
        <h3>No Assignment Flight List</h3>
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
                <td>{flight.departure_time ? new Date(flight.departure_time).toLocaleString() : '-'}</td>
                <td>{flight.arrival_time ? new Date(flight.arrival_time).toLocaleString() : '-'}</td>
                <td>{flight.status}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else if !errorMessage_records && !$loading}
        <p>There is no non-assignment flight!</p>
      {/if}
    </div>
  </div>
</div>
</div>
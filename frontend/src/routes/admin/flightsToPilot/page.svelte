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

  // Variables for pilot and flight assignment
  let pilot_id = '';
  let flight_id = '';

  // No-assigned flights
  let no_assign_flights = [];

  // Available spaceships
  let available_spaceships = [];

  // Navigate to home
  function navigateHome() {
    navigate('/');
  }

  // 조종사 비행 할당 (Assign Pilot to Flight)
  async function CombinePilotFlight(event) {
    event.preventDefault();
    loading.set(true);
    errorMessage = '';

    const endpoint = 'http://localhost:8000/pilot_flights/pilot_assignment/';

    const payload = {
      pilot_id: parseInt(pilot_id),
      flight_id: parseInt(flight_id)
    };

    try {
      const response = await axios.post(endpoint, payload);
      if (response.data) {
        console.log('추가된 기록:', response.data);
        // 입력 필드 초기화
        pilot_id = '';
        flight_id = '';
        // 유지보수 작업 목록 갱신
        findFlightsNoPilot();
      } else {
        errorMessage = '유지보수 기록을 추가할 수 없습니다.';
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

  // Fetch available spaceships
  async function findSpaceshipAdmin() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_spaceships = 'http://localhost:8000/available_spaceships'; // Adjust the endpoint as needed

    try {
      const response = await axios.get(endpoint_spaceships);
      if (Array.isArray(response.data)) {
        available_spaceships = response.data;
        console.log('Available spaceships:', available_spaceships);
      } else {
        errorMessage_get = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('Available spaceships 데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        errorMessage_get = `서버 오류 발생: ${error.response.status}`;
      } else {
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    findFlightsNoPilot(); // Optionally fetch unassigned flights on mount
  });
</script>

<style>
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
</style>

<div class="mechanic-page">
  <h1>비행과 유지보수일정 생성</h1>
  <p>관리자 ID: {adminId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>

  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  <div class="records-section">
    <!-- Flight Creation -->

    <!-- Unassigned Flights List -->
    <div>
      {#if no_assign_flights.length > 0}
        <h3>할당되지 않은 비행 목록</h3>
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
        <p>할당되지 않은 비행이 없습니다.</p>
      {/if}
    </div>
  </div>

  <!-- 할당하기 (Assign Pilot to Flight) -->
  <div>
    <h2>Flight 생성</h2>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    <form on:submit={CombinePilotFlight}>
      <label for="pilot_id">Pilot ID:</label>
      <input type="number" id="pilot_id" bind:value={pilot_id} placeholder="Pilot ID" required />

      <label for="flight_id">Flight ID:</label>
      <input type="number" id="flight_id" bind:value={flight_id} placeholder="Flight ID" required />

      <button type="submit">조종사 할당</button>
    </form>
  </div>
</div>

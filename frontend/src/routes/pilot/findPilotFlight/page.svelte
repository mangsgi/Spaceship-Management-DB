<!-- src/routes/pilot/findPilotFlight.svelte -->
<script>
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  let pilotId;
  $: pilotId = $userId;

  const loading = writable(false);
  let errorMessage = '';
  let data = [];

  async function findMyFlight() {
    loading.set(true);
    errorMessage = '';

    const endpoint = 'http://localhost:8000/flights_by_pilot';

    try {
      const response = await axios.get(endpoint, { params: { pilot_id: pilotId } });

      if (response.data && Array.isArray(response.data)) {
        data = response.data;
        console.log('결과 : ', data);
      } else {
        errorMessage = '서버에서 올바른 데이터를 받지 못했습니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
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

  onMount(() => {
    console.log('FindPilotFlight 컴포넌트가 마운트되었습니다.');
    findMyFlight();
  });
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  .pilot-page {
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

  .pilot-container {
    background-color: rgba(0, 0, 0, 0.6); /* 반투명 배경 */
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
  }

  h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
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

  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 100%;
    color: white;
  }

  th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }

  th {
    background: #333;
  }

  button {
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
    margin: 10px 0;
    padding: 10px 20px;
    border-radius: 50px;
    border: 2px solid white;
    background-color: transparent;
    color: white;
    transition: background-color 0.3s, color 0.3s;
    width: 100%;
    cursor: pointer;
  }

  button:hover {
    background-color: white;
    color: black;
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
</style>

<div class="pilot-page">
  <div class="pilot-container">
    <h1>Find Pilot's Flight</h1>
    <p>Pilot ID: {pilotId}</p>
    <button on:click={() => navigate('/pilot')}>Back to Menu
    </button>

    {#if $loading}
      <p class="loading">Loading...</p>
    {/if}

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}

    {#if data.length > 0}
      <h2>Flight</h2>
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
          {#each data as flight}
            <tr>
              <td>{flight.flight_id}</td>
              <td>{flight.spaceship_id}</td>
              <td>{flight.departure_location}</td>
              <td>{flight.arrival_location}</td>
              <td>{new Date(flight.departure_time).toLocaleString()}</td>
              <td>{new Date(flight.arrival_time).toLocaleString()}</td>
              <td>{flight.status}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else if !$loading && !errorMessage}
      <p>No flight data available.</p>
    {/if}
  </div>
</div>

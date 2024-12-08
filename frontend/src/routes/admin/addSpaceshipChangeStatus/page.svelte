<!-- src/routes/mechanic/page.svelte -->
<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { navigate } from 'svelte-routing'; // 또는 사용 중인 라우팅 라이브러리에 맞게 조정
  import { userId } from '../../../stores.js'; // 경로를 필요에 맞게 조정
  import axios from 'axios';

  // Loading and error states
  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';
  let errorMessage_records = '';

  // 구독을 위해 $를 사용하지 않고 adminId를 선언
  let adminId;
  $: adminId = $userId;

  // Variables for spaceship creation
  let model = '';
  let manufacture_date = '';
  let spaceship_status = '';
  let last_maintenance_date = '';

  // Available spaceships
  let available_spaceships = [];

  // Navigate to home
  function navigateHome() {
    navigate('/');
  }

  // 우주선 생성 (Create Spaceship)
  async function createSpaceship(event) {
    event.preventDefault();
    loading.set(true);
    errorMessage = '';

    const endpoint = 'http://localhost:8000/spaceships';

    const payload = {
      model: model, // model_name -> model 으로 수정
      manufacture_date: manufacture_date,
      status: spaceship_status, // '운영 중' 등
      last_maintenance_date: last_maintenance_date
    };

    try {
      const response = await axios.post(endpoint, payload);
      if (response.data) {
        console.log('추가된 우주선:', response.data);
        // 입력 필드 초기화
        model = '';
        manufacture_date = '';
        spaceship_status = '';
        last_maintenance_date = '';
        // 우주선 목록 갱신
        fetchAvailableSpaceships();
      } else {
        errorMessage = '우주선을 추가할 수 없습니다.';
      }
    } catch (error) {
      console.error('우주선을 추가하는 중 오류 발생:', error);
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

  // Fetch available spaceships
  async function fetchAvailableSpaceships() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_spaceships = 'http://localhost:8000/spaceships/available'; // 필요에 따라 엔드포인트 조정

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
    fetchAvailableSpaceships(); // 컴포넌트 마운트 시 우주선 목록을 가져옴
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
  form input, form textarea, form select {
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



<div class="admin-page">
<div class="admin-container">
  <h1>Add Spaceship & Change Status</h1>
  <p>Admin ID: {adminId}</p>
  <button on:click={() => navigate("/admin")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  <div class="record-section">
    <!-- Available Spaceships List -->
    <div>
      {#if available_spaceships.length > 0}
        <h3>Available Spaceship List</h3>
        <table>
          <thead>
            <tr>
              <th>Spaceship ID</th>
              <th>Model Name</th>
              <th>Manufacture Date</th>
              <th>Status</th>
              <th>Last Maintenance Date</th>
            </tr>
          </thead>
          <tbody>
            {#each available_spaceships as spaceship}
              <tr>
                <td>{spaceship.spaceship_id}</td>
                <td>{spaceship.model}</td>
                <td>{new Date(spaceship.manufacture_date).toLocaleDateString()}</td>
                <td>{spaceship.status}</td>
                <td>{new Date(spaceship.last_maintenance_date).toLocaleDateString()}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else if !errorMessage_get && !$loading}
        <p>There is no available spaceship.</p>
      {/if}

      {#if errorMessage_get}
        <p class="error">{errorMessage_get}</p>
      {/if}
    </div>
  
</div>

  <!-- 우주선 생성 폼 -->
  <div>
    <h2>Add Spaceship</h2>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    <form on:submit={createSpaceship}>
      <label for="model">Model Name:</label>
      <input type="text" id="model" bind:value={model} placeholder="Model Name" required />

      <label for="manufacture_date">Manufacture Date:</label>
      <input type="date" id="manufacture_date" bind:value={manufacture_date} required />

      <label for="spaceship_status">Status:</label>
      <select id="spaceship_status" bind:value={spaceship_status} required>
        <option value="" disabled selected>Choose Status</option>
        <option value="운영 중">운영 중</option>
        <option value="정비 중">점검 중</option>
      </select>

      <label for="last_maintenance_date">Last Maintenance Date:</label>
      <input type="date" id="last_maintenance_date" bind:value={last_maintenance_date} required />

      <button type="submit">Add</button>
    </form>
  </div>
  </div>
</div>

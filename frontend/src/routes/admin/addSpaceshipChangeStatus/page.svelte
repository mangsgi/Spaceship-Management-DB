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
</style>

<div class="mechanic-page">
  <h1>우주선 생성 및 관리</h1>
  <p>관리자 ID: {adminId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>

  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  <div class="records-section">
    <!-- Available Spaceships List -->
    <div>
      {#if available_spaceships.length > 0}
        <h3>사용 가능한 우주선 목록</h3>
        <table>
          <thead>
            <tr>
              <th>우주선 ID</th>
              <th>모델</th>
              <th>제조일</th>
              <th>상태</th>
              <th>최종 유지보수일</th>
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
        <p>사용 가능한 우주선이 없습니다.</p>
      {/if}

      {#if errorMessage_get}
        <p class="error">{errorMessage_get}</p>
      {/if}
    </div>
  </div>

  <!-- 우주선 생성 폼 -->
  <div>
    <h2>우주선 생성</h2>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    <form on:submit={createSpaceship}>
      <label for="model">모델:</label>
      <input type="text" id="model" bind:value={model} placeholder="모델명" required />

      <label for="manufacture_date">제조일:</label>
      <input type="date" id="manufacture_date" bind:value={manufacture_date} required />

      <label for="spaceship_status">상태:</label>
      <select id="spaceship_status" bind:value={spaceship_status} required>
        <option value="" disabled selected>상태 선택</option>
        <option value="운영 중">운영 중</option>
        <option value="정비 중">점검 중</option>
      </select>

      <label for="last_maintenance_date">최종 유지보수일:</label>
      <input type="date" id="last_maintenance_date" bind:value={last_maintenance_date} required />

      <button type="submit">우주선 생성</button>
    </form>
  </div>
</div>

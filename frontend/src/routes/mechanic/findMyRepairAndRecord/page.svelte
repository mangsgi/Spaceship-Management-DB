<!-- src/routes/mechanic/page.svelte -->
<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { navigate } from "svelte-routing"; // SvelteKit 사용 시 다른 네비게이션 방식 필요
  import { userId } from "../../../stores.js"; // 경로 조정
  import axios from "axios";

  // 로딩, 에러 메시지
  const loading = writable(false);
  let errorMessage = "";
  let errorMessage_get = "";

  // 유지보수 작업 목록
  let tasks = [];
  $: mechanicId = $userId;

  // 유지보수 기록 추가용 필드
  let task_id = "";
  let details = "";
  let parts_used = "";
  let time_spent = "";

  // 유지보수 기록 조회용 필드
  let record_id = "";
  let maintenanceRecords = []; // 조회된 유지보수 기록을 저장할 배열
  let errorMessage_records = "";

  // 홈으로 이동
  function navigateHome() {
    navigate("/");
  }

  // 유지보수 작업 조회 함수
  async function findMyTask() {
    loading.set(true);
    errorMessage_get = "";

    const endpoint_get = "http://localhost:8000/maintenance_tasks/mechanic";

    try {
      const response = await axios.get(endpoint_get, {
        params: { mechanic_id: mechanicId },
      });
      if (Array.isArray(response.data)) {
        const matchedItems = response.data;
        if (matchedItems.length > 0) {
          tasks = matchedItems;
        } else {
          errorMessage_get = "해당 작업을 찾을 수 없습니다.";
        }
      } else {
        errorMessage_get = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error("데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_get = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  // 유지보수 기록 추가
  async function addRecords(event) {
    event.preventDefault();
    loading.set(true);
    errorMessage = "";

    const endpoint = "http://localhost:8000/maintenance_records";

    const payload = {
      task_id: parseInt(task_id),
      details,
      parts_used,
      time_spent: parseFloat(time_spent),
    };

    try {
      const response = await axios.post(endpoint, payload);
      if (response.data) {
        console.log("추가된 기록:", response.data);
        // 입력 필드 초기화
        task_id = "";
        details = "";
        parts_used = "";
        time_spent = "";
        // 유지보수 작업 목록 갱신
        findMyTask();
        // 기록 조회 갱신 (필요시)
        if (record_id) {
          findRecords();
        }
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

  // 유지보수 기록 조회 함수
  async function findRecords() {
    loading.set(true);
    errorMessage_records = "";

    const endpoint_records = "http://localhost:8000/maintenance_records";

    // record_id가 비어있다면 전체 기록 조회 혹은 에러 표시
    const params = {};
    if (record_id) {
      params.record_id = parseInt(record_id);
    }

    try {
      const response = await axios.get(endpoint_records, { params });
      if (Array.isArray(response.data)) {
        // 배열 형태라면 바로 저장
        maintenanceRecords = response.data;
      } else if (response.data) {
        // 단일 객체로 응답 시 배열로 변환
        maintenanceRecords = [response.data];
      } else {
        errorMessage_records = "유지보수 기록을 찾을 수 없습니다.";
      }
    } catch (error) {
      console.error("유지보수 기록 가져오는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_records = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
        } else if (error.response.status === 404) {
          errorMessage_records = "해당 기록을 찾을 수 없습니다.";
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

  onMount(() => {
    findMyTask();
  });
</script>

<div class="mechanic-page">
  <div class="mechanic-container">
  <h1>Find My Task & Records</h1>
  <p>Mechanic ID: {mechanicId}</p>
  <button on:click={() => navigate("/mechanic")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  <!-- 유지보수 작업 목록 -->
  {#if tasks.length > 0}
    <h2>Task List</h2>
    <table>
      <thead>
        <tr>
          <th>Task ID</th>
          <th>Spaceship ID</th>
          <th>Task Type</th>
          <th>Priority</th>
          <th>Deadline</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {#each tasks as task}
          <tr>
            <td>{task.task_id}</td>
            <td>{task.spaceship_id}</td>
            <td>{task.task_type}</td>
            <td>{task.priority}</td>
            <td>{new Date(task.deadline).toLocaleDateString()}</td>
            <td>{task.status}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else if !errorMessage_get && !$loading}
    <p>No Task!</p>
  {/if}

  <div class="records-section">
    <!-- 유지보수 기록 추가 폼 -->
    <div>
      <h2>Add Task's Records</h2>
      {#if errorMessage}
        <p class="error">{errorMessage}</p>
      {/if}
      <form on:submit={addRecords}>
        <label for="task_id">Task ID:</label>
        <input
          type="number"
          id="task_id"
          bind:value={task_id}
          placeholder="Task ID"
          required
        />

        <label for="details">Details:</label>
        <textarea
          id="details"
          bind:value={details}
          placeholder="Details"
          required
        ></textarea>

        <label for="parts_used">Parts Used:</label>
        <input
          type="text"
          id="parts_used"
          bind:value={parts_used}
          placeholder="Parts Used"
          required
        />

        <label for="time_spent">Time Spent (hours):</label>
        <input
          type="number"
          step="0.1"
          id="time_spent"
          bind:value={time_spent}
          placeholder="Time Spent"
          required
        />

        <button type="submit">Add</button>
      </form>
    </div>

    <!-- 유지보수 기록 조회 -->
    <div>
      <h2>Search My Records</h2>
      {#if errorMessage_records}
        <p class="error">{errorMessage_records}</p>
      {/if}
      <form on:submit|preventDefault={findRecords}>
        <label for="record_id">Record ID(Option):</label>
        <input
          type="number"
          id="record_id"
          bind:value={record_id}
          placeholder="Record ID"
        />
        <button type="submit">Search</button>
      </form>

      {#if maintenanceRecords.length > 0}
        <h3>Record List</h3>
        <table>
          <thead>
            <tr>
              <th>Record ID</th>
              <th>Task ID</th>
              <th>Details</th>
              <th>Parts Used</th>
              <th>Time Spent</th>
              <th>Date Created</th>
            </tr>
          </thead>
          <tbody>
            {#each maintenanceRecords as record}
              <tr>
                <td>{record.record_id}</td>
                <td>{record.task_id}</td>
                <td>{record.details}</td>
                <td>{record.parts_used}</td>
                <td>{record.time_spent}</td>
                <td
                  >{record.date_created
                    ? new Date(record.date_created).toLocaleString()
                    : ""}</td
                >
              </tr>
            {/each}
          </tbody>
        </table>
      {:else if !errorMessage_records && !$loading}
        <p>No Records!</p>
      {/if}
    </div>
  </div>
</div>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap");

  .mechanic-page {
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

.mechanic-container {
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

<!-- src/routes/pilot/page.svelte -->
<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
  $: mechanicId = $userId;

  async function findMyTask() {

    loading.set(true);

    let endpoint_get = 'http://localhost:8000/maintenance_tasks/mechanic'; // 미구현

    try {
      const response = await axios.get(endpoint_get, { params: { mechanic_id: mechanicId } });

      // 임시 조건 (실제 응답 검증으로 대체)
      if (response.data && response.data.mechanic_id === mechanicId) {
        // 역할에 따른 URL로 네비게이션
        data_get = response.data;
        
      } 
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  } 

async function updatePilotInfo() {

loading.set(true);
errorMessage = '';

//여기부터
const endpoint = `http://localhost:8000/pilots/${pilotId}`;

// 전송할 데이터 정의 (예: 업데이트할 파일럿 정보)
const payload = {
  name,
  contact_info,
  emergency_contact,
};

try {
  const response = await axios.patch(endpoint, payload);

  // 임시 조건 (실제 응답 검증으로 대체)
  if (response.data) {
    data.push(response.data); // 새로 업데이트된 비행 정보를 data 배열에 추가
    console.log('결과:', response.data);
    data_get = response.data;
  } else {
    console.log('Received data:', response.data);
    errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
  }
} catch (error) {
  console.error('데이터를 가져오는 중 오류 발생:', error);
  if (error.response) {
    // 서버 응답 오류 처리
    if (error.response.status === 400) {
      errorMessage = '잘못된 요청입니다. 입력 데이터를 확인해주세요.';
    } else if (error.response.status === 422) {
      errorMessage = '서버가 요청을 이해했으나 처리할 수 없습니다. 요청 데이터를 확인해주세요.';
    } else if (error.response.status === 404) {
      errorMessage = '해당 파일럿을 찾을 수 없습니다.';
    } else {
      errorMessage = `서버 오류 발생: ${error.response.status}`;
    }
  } else {
    // 요청이 서버에 도달하지 못한 경우
    errorMessage = '서버에 연결할 수 없습니다.';
  }
} finally {
  loading.set(false);
}
}
</script>

<style>
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
</style>

<div class="pilot-page">
  <h1>본인 수리 조회 및 해당 수리에 대한 유지보수 작성</h1>
  <p>파일럿 ID: {mechanicId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 파일럿 관련 내용 추가 -->

    <!-- 데이터 표시를 위한 테이블 구조 -->
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
        <!-- {
          "task_id": 1,
          "spaceship_id": 1,
          "task_type": "정기 점검",
          "priority": 1,
          "deadline": "2026-11-24",
          "status": "대기 중" // "뺄수도 있다"
      } -->
        {#each data as flight}
          <tr>
            <td>{mytask.task_id}</td>
            <td>{mytask.spaceship_id}</td>
            <td>{mytask.task_type}</td>
            <td>{mytask.priority}</td>
            <td>{new Date(flight.deadline).toLocaleString()}</td>
            <td>{mytask.status}</td>
          </tr>
        {/each}
      </tbody>
    </table>
</div>

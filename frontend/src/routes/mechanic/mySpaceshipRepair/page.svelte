<script>
  import { userId } from "../../../stores.js"; // 경로에 따라 조정
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing"; // Ensure this is appropriate for your setup
  import { writable } from "svelte/store";
  import axios from "axios";

  let mechanicId;
  $: mechanicId = $userId; // $userId 값이 변경될 때 mechanicId도 갱신됨

  const loading = writable(false);
  let errorMessage = "";

  let maintenanceTasks = [];
  let spaceshipData = [];

  async function fetchMaintenanceTasks() {
    loading.set(true);
    let endpoint = "http://localhost:8000/maintenance_tasks/mechanic";

    try {
      const response = await axios.get(endpoint, {
        params: { mechanic_id: mechanicId },
      });

      if (response.data && Array.isArray(response.data)) {
        maintenanceTasks = response.data;

        // 중복 spaceship_id를 제거하기 위해 Set 사용
        const spaceshipIds = [
          ...new Set(maintenanceTasks.map((task) => task.spaceship_id)),
        ];

        // 우주선 정보 가져오기
        await fetchSpaceshipData(spaceshipIds);
      }
    } catch (error) {
      console.error("데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  async function fetchSpaceshipData(spaceshipIds) {
    try {
      // 여러 우주선 정보를 비동기로 가져온 뒤, 모두 Promise.all로 처리
      const promises = spaceshipIds.map(async (id) => {
        const res = await axios.get("http://localhost:8000/spaceships", {
          params: { spaceship_id: id },
        });
        return res.data; // 각 응답은 배열 형태
      });

      const results = await Promise.all(promises);
      // 모든 결과를 하나의 배열로 합침
      spaceshipData = results.flat();
    } catch (error) {
      console.error("우주선 데이터를 가져오는 중 오류 발생:", error);
    }
  }

  onMount(() => {
    console.log("컴포넌트가 마운트되었습니다.");
    fetchMaintenanceTasks();
  });
</script>

<div class="mechanic-page">
  <div class="mechanic-container">
  <h2>Search Spaceship Status</h2>
  <p>Mechanic ID: {mechanicId}</p>
  <button on:click={() => navigate("/mechanic")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}

  <!-- 우주선 정보 표시 테이블 -->
  {#if spaceshipData.length > 0}
    <h3>Reparing Spaceship Info</h3>
    <table>
      <thead>
        <tr>
          <th>Spaceship ID</th>
          <th>Model</th>
          <th>Manufacture Date</th>
          <th>Status</th>
          <th>Last Maintenance Date</th>
        </tr>
      </thead>
      <tbody>
        {#each spaceshipData as spaceship}
          <tr>
            <td>{spaceship.spaceship_id}</td>
            <td>{spaceship.model}</td>
            <td>{new Date(spaceship.manufacture_date).toLocaleDateString()}</td>
            <td>{spaceship.status}</td>
            <td
              >{new Date(
                spaceship.last_maintenance_date,
              ).toLocaleDateString()}</td
            >
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
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

<!-- <style>
  .page {
    text-align: center;
    padding: 50px;
  }
  table {
    border-collapse: collapse;
    margin: 20px auto;
  }
  th,
  td {
    border: 1px solid #333;
    padding: 10px;
  }
  .error {
    color: red;
  }
  .loading {
    font-style: italic;
  }
</style> -->

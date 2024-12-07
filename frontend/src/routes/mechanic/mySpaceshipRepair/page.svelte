<script>
  import { userId } from '../../../stores.js'; // 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  let mechanicId;
  $: mechanicId = $userId;  // $userId 값이 변경될 때 mechanicId도 갱신됨

  const loading = writable(false);
  let errorMessage = '';

  let maintenanceTasks = [];
  let spaceshipData = [];

  async function fetchMaintenanceTasks() {
    loading.set(true);
    let endpoint = 'http://localhost:8000/maintenance_tasks/mechanic';

    try {
      const response = await axios.get(endpoint, { params: { mechanic_id: mechanicId } });

      if (response.data && Array.isArray(response.data)) {
        maintenanceTasks = response.data;

        // 중복 spaceship_id를 제거하기 위해 Set 사용
        const spaceshipIds = [...new Set(maintenanceTasks.map(task => task.spaceship_id))];

        // 우주선 정보 가져오기
        await fetchSpaceshipData(spaceshipIds);
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
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

  async function fetchSpaceshipData(spaceshipIds) {
    try {
      // 여러 우주선 정보를 비동기로 가져온 뒤, 모두 Promise.all로 처리
      const promises = spaceshipIds.map(async id => {
        const res = await axios.get('http://localhost:8000/spaceships', { params: { spaceship_id: id } });
        return res.data; // 각 응답은 배열 형태
      });

      const results = await Promise.all(promises);
      // 모든 결과를 하나의 배열로 합침
      spaceshipData = results.flat();
    } catch (error) {
      console.error('우주선 데이터를 가져오는 중 오류 발생:', error);
    }
  }

  onMount(() => {
    console.log('컴포넌트가 마운트되었습니다.');
    fetchMaintenanceTasks();
  });
</script>

<style>
.page {
  text-align: center;
  padding: 50px;
}
table {
  border-collapse: collapse;
  margin: 20px auto;
}
th, td {
  border: 1px solid #333;
  padding: 10px;
}
.error {
  color: red;
}
.loading {
  font-style: italic;
}
</style>

<div class="page">
  <h2>우주선 정보 조회</h2>
  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}

  <!-- 우주선 정보 표시 테이블 -->
  {#if spaceshipData.length > 0}
    <h3>작업중인 우주선 정보</h3>
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
            <td>{new Date(spaceship.last_maintenance_date).toLocaleDateString()}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

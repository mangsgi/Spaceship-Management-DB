<!-- src/routes/pilot/page.svelte -->
<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
  $: pilotId = $userId;
</script>

<style>
  .pilot-page {
    text-align: center;
    padding: 50px;
  }
  .pilot-page button {
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
  <h1>파일럿 페이지</h1>
  <p>파일럿 ID: {pilotId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 파일럿 관련 내용 추가 -->

  <div>
    <h3>골라 들어가기</h3>
    <Link to="/pilot/findPilotFlight">
      <button>본인 정보 조회</button>
    </Link>
    <Link to="/pilot/updatePilotInfo">
      <button>내정보 수정</button>
    </Link>
    <Link to="/pilot/updateLicense">
      <button>라이센스 갱신</button>
    </Link>
  </div>
</div>

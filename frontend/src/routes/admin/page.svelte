<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  $: adminId = $userId;
</script>

<style>
  .admin-page {
    text-align: center;
    padding: 50px;
  }
  .admin-page button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    cursor: pointer;
  }
</style>

<div class="admin-page">
  <h2>관리자 페이지</h2>
  <p>관리자 ID: {adminId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 정비사 관련 내용 추가 -->

  <div>
    <h3>골라 들어가기</h3>
    <Link to="/admin/addFlightAndRecords">
      <button>비행, 유지보수일정,생성</button>
    </Link>
    <Link to="/admin/flightsToPilot">
      <button>조종사 비행 할당</button>
    </Link>
    <Link to="/admin/addSpaceshipChangeStatus">
      <button>우주선 생성 및 상태 변경 </button> <!-- 최근 유지보수 일 생성으로 인한 아직은 미구현-->
    </Link>
    <Link to="/admin/changeLicenseStatus">
      <button>라이센스 상태 변경(조회 수정)</button>
    </Link>
  </div>
</div>

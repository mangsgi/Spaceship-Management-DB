<!-- src/App.svelte -->
<script>
  import { Router, Route, navigate } from 'svelte-routing';
  import Home from './routes/Home.svelte';
  import Login from './routes/Login.svelte';
  import Pilot from './routes/pilot/page.svelte';
  import FindPilotFlight from './routes/pilot/findPilotFlight/page.svelte';
  import UpdatePilotInfo from './routes/pilot/updatePilotInfo/page.svelte';
  import UpdateLicense from './routes/pilot/updateLicense/page.svelte';
  import Mechanic from './routes/mechanic/page.svelte';
  import Customer from './routes/customer/page.svelte';
  import Admin from './routes/admin/page.svelte';
</script>

<Router>
  <Route path="/" component={Home} />
  <Route path="/login" component={Login} />
  <Route path="/pilot" component={Pilot} />
  <Route path="/pilot/findPilotFlight" component={FindPilotFlight} />
  <Route path="/pilot/updatePilotInfo" component={UpdatePilotInfo} />
  <Route path="/pilot/updateLicense" component={UpdateLicense} />
  <Route path="/mechanic" component={Mechanic} />
  <Route path="/customer" component={Customer} />
  <Route path="/admin" component={Admin} />
  <!-- 추가적인 라우트 설정 -->
</Router>

<style>
  .page {
    text-align: center;
    padding: 50px;
  }
  button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  input {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .loading {
    font-style: italic;
  }
</style>

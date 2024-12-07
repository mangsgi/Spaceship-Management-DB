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
  import FindMyRepairAndRecord from './routes/mechanic/findMyRepairAndRecord/page.svelte';
  import MySpaceshipRepair from './routes/mechanic/mySpaceshipRepair/page.svelte';
  import Customer from './routes/customer/page.svelte';
  import FindFlightsAndAddReservation from './routes/customer/findFlightsAndAddReservation/page.svelte';
  import FindMyReservationAndCancel from './routes/customer/findMyReservationAndCancel/page.svelte';
  import UpdateCustomInfo from './routes/customer/updateCustomInfo/page.svelte';
  import Admin from './routes/admin/page.svelte';
  import AddFlightAndRecords from './routes/admin/addFlightAndRecords/page.svelte';
  import FlightsToPilot from './routes/admin/flightsToPilot/page.svelte';
  import AddSpaceshipChangeStatus from './routes/admin/addSpaceshipChangeStatus/page.svelte';
  import ChangeLicenseStatus from './routes/admin/changeLicenseStatus/page.svelte';
</script>

<Router>
  <Route path="/" component={Home} />
  <Route path="/login" component={Login} />
  <Route path="/pilot" component={Pilot} />
  <Route path="/pilot/findPilotFlight" component={FindPilotFlight} />
  <Route path="/pilot/updatePilotInfo" component={UpdatePilotInfo} />
  <Route path="/pilot/updateLicense" component={UpdateLicense} />
  <Route path="/mechanic" component={Mechanic} />
  <Route path="/mechanic/findMyRepairAndRecord" component={FindMyRepairAndRecord} />
  <Route path="/mechanic/mySpaceshipRepair" component={MySpaceshipRepair} />
  <Route path="/customer" component={Customer} />
  <Route path="/customer/findFlightsAndAddReservation" component={FindFlightsAndAddReservation} />
  <Route path="/customer/findMyReservationAndCancel" component={FindMyReservationAndCancel} />
  <Route path="/customer/updateCustomInfo" component={UpdateCustomInfo} />
  <Route path="/admin/" component={Admin} />
  <Route path="/admin/addFlightAndRecords" component={AddFlightAndRecords} />
  <Route path="/admin/flightsToPilot" component={FlightsToPilot} />
  <Route path="/admin/addSpaceshipChangeStatus" component={AddSpaceshipChangeStatus} />
  <Route path="/admin/changeLicenseStatus" component={ChangeLicenseStatus} />
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

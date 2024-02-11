import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Box, Typography } from "@mui/material";
import TrafficLight from "./components/TrafficLight";
import { useEffect, useState } from "react";

function App() {
  const [services, setServices] = useState<any>();
  const [configData, setConfigData] = useState<any>();

  async function getConfig() {
    const response = await fetch(`http://localhost:8000/api/v1/config`);
    setConfigData(await response.json());
  }

  async function getServicesState() {
    const response = await fetch(`http://localhost:8000/api/v1/services`);
    setServices(await response.json());
  }

  const convertIsoString = (isoDatetimeString: string): string => {
    let date = new Date(isoDatetimeString);
    return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
  };

  const getTrafficLight = (trafficLightValue: string): any => {
    switch (trafficLightValue) {
      case "red":
        return <TrafficLight color="red" />;
      case "yellow":
        return <TrafficLight color="yellow" />;
      case "green":
        return <TrafficLight color="green" />;
      default:
        return <TrafficLight color="grey" />;
    }
  };

  useEffect(() => {
    // ? https://rapidapi.com/guides/api-requests-intervals
    // TODO prevent making double requests on page load

    let interval = setInterval(getServicesState, 5000);
    getServicesState();
    if (!configData) getConfig();

    return () => {
      clearInterval(interval);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tableHeaderStyle = {
    color: "white",
    fontWeight: "bold",
    fontSize: "15px",
  };

  return (
    <Box>
      <Typography
        variant="h3"
        sx={{ textAlign: "center", marginTop: "30px", marginBottom: "30px" }}
      >
        Web Health Checker
      </Typography>

      <TableContainer component={Paper} sx={{ backgroundColor: "#555a64" }}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell sx={tableHeaderStyle}>url</TableCell>
              <TableCell align="center" sx={tableHeaderStyle}>
                Response time [ms]
              </TableCell>
              <TableCell align="center" sx={tableHeaderStyle}>
                Last updated
              </TableCell>
              <TableCell align="left" sx={tableHeaderStyle}>
                State
              </TableCell>
              <TableCell align="left" sx={tableHeaderStyle}>
                Details
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {configData &&
              configData.map((row: any) => {
                let service = undefined;
                if (services)
                  service = services.find((el: any) => el.index === row.index);

                return (
                  <TableRow
                    key={row.index}
                    sx={{
                      "&:last-child td, &:last-child th": { border: 0 },
                      color: "white",
                    }}
                  >
                    <TableCell
                      component="th"
                      scope="row"
                      sx={{ color: "white" }}
                    >
                      {row.url}
                    </TableCell>
                    <TableCell align="center" sx={{ color: "white" }}>
                      {service
                        ? service.response_time_miliseconds
                          ? service.response_time_miliseconds
                          : "---"
                        : "---"}
                    </TableCell>
                    <TableCell
                      align="center"
                      sx={{ color: "white", minWidth: "150px" }}
                    >
                      {service ? convertIsoString(service.last_updated) : ""}
                    </TableCell>
                    <TableCell
                      className="stateValueCell"
                      sx={{ color: "white" }}
                    >
                      {service ? (
                        getTrafficLight(service.state)
                      ) : (
                        <TrafficLight color="grey" />
                      )}
                    </TableCell>
                    <TableCell
                      align="left"
                      sx={{ color: "white", maxWidth: "600px" }}
                    >
                      {service ? service.details : ""}
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default App;

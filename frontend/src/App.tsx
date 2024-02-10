import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { Box, Typography } from "@mui/material";
import { useEffect, useState } from 'react';
import './App.css';


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
    let date = isoDatetimeString.split('T')[0];
    let time = isoDatetimeString.split('T')[1].split('.')[0];   // time without miliseconds
    return `${date} ${time}`;
  }

  useEffect(() => {
    // ? https://rapidapi.com/guides/api-requests-intervals
    // TODO prevert making double requests on page load
  
    let interval = setInterval(getServicesState, 5000);
    getServicesState();
    if(!configData) getConfig();

    return () => {
      clearInterval(interval);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box>
      <Typography variant="h3" sx={{textAlign: 'center', marginTop: '30px', marginBottom: '30px'}}>
        Web Health Checker
      </Typography>

      <TableContainer component={Paper}  sx={{backgroundColor: "#555a64", color: 'white'}}>
        <Table sx={{ minWidth: 650,  color: 'white' }} aria-label="simple table" >
          <TableHead>
            <TableRow>
              <TableCell sx={{color: 'white'}}>url</TableCell>
              <TableCell align="right" sx={{color: 'white'}}>Expected code</TableCell>
              <TableCell align="right" sx={{color: 'white'}}>Last updated</TableCell>
              <TableCell align="right" sx={{color: 'white'}}>State</TableCell>
              <TableCell align="right" sx={{color: 'white'}}>Details</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {configData && configData.map((row: any) => {
              let service = undefined;
              if (services) service = services.find((el: any) => el.index === row.index);
              
              return (
                <TableRow
                  key={row.index}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 }, color: 'white' }}
                >
                  <TableCell component="th" scope="row" sx={{color: 'white'}}>{row.url}</TableCell>
                  <TableCell align="right" sx={{color: 'white'}}>{row.expected_status_code}</TableCell>
                  <TableCell align="right" sx={{color: 'white'}}>{service ? convertIsoString(service.last_updated) : ''}</TableCell>
                  <TableCell align="right" sx={{color: 'white'}}>{service ? service.state : ''}</TableCell>
                  <TableCell align="right" sx={{color: 'white'}}>{service ? service.details : ''}</TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default App;

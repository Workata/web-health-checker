import React from 'react';
import {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


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
    // let date: Date = new Date(isoDatetimeString);
    // return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    let date = isoDatetimeString.split('T')[0];
    let time = isoDatetimeString.split('T')[1].split('.')[0];   // time without miliseconds
    return `${date} ${time}`;
  }

  useEffect(() => {
    // ? https://rapidapi.com/guides/api-requests-intervals
    let interval = setInterval(getServicesState, 5000);
    if(!configData) getConfig();

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    //  sx={{backgroundColor: "#555a64"}}
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>url</TableCell>
            <TableCell align="right">Expected code</TableCell>
            <TableCell align="right">Last updated</TableCell>
            <TableCell align="right">State</TableCell>
            <TableCell align="right">Details</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {configData && configData.map((row: any) => {
            let service = undefined;
            if (services) service = services.find((el: any) => el.index == row.index);
            
            return (
              <TableRow
                key={row.index}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">{row.url}</TableCell>
                <TableCell align="right">{row.expected_status_code}</TableCell>
                <TableCell align="right">{service ? convertIsoString(service.last_updated) : ''}</TableCell>
                <TableCell align="right">{service ? service.state : ''}</TableCell>
                <TableCell align="right">{service ? service.details : ''}</TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default App;

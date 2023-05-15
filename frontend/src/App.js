import React, { useState } from 'react';
import * as XLSX from 'xlsx';

function ExcelParser() {
  const [userData, setUserData] = useState([]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      const data = e.target.result;
      const workbook = XLSX.read(data, { type: 'binary' });
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      const usernameColumn = 'username'; // Replace with your desired column name

      const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      const headerRow = rows[0];
      const usernameColumnIndex = headerRow.findIndex((cell) => cell === usernameColumn);

      if (usernameColumnIndex !== -1) {
        const userData = rows.slice(1).map((row) => row[usernameColumnIndex]);
        setUserData(userData);
      } else {
        console.log(`Column "${usernameColumn}" not found`);
      }
    };

    reader.readAsBinaryString(file);
  };

  return (
    <div>
      <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} />
      <ul>
        {userData.map((username, index) => (
          <li key={index}>{username}</li>
        ))}
      </ul>
    </div>
  );
}

export default ExcelParser;

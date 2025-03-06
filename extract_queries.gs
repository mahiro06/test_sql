function extractQueriesFromGitHub() {
  const env = PropertiesService.getScriptProperties().getProperty('ENV_FILE_PATH');
  const envVars = parseEnvFile(env);
  const accessToken = envVars['GITHUB_ACCESS_TOKEN'];
  const sheetId = '1YZhnXzg6lVC_7hhAr5ZZnxwJn7rqrF-avdWHZY4VAiw';
  const sheetName = 'Queries';
  
  const url = `https://api.github.com/repos/mahiro06/test_sql/contents/`;
  const headers = {
    'Authorization': `token ${accessToken}`,
    'Accept': 'application/vnd.github.v3+json'
  };
  
  const response = UrlFetchApp.fetch(url, { headers });
  const files = JSON.parse(response.getContentText());
  
  const sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName);
  const existingData = sheet.getDataRange().getValues();
  const existingEntries = new Set(existingData.map(row => row.join(',')));
  
  let row = existingData.length + 1;
  files.forEach(file => {
    if (file.name.endsWith('.sql')) {
      const fileContent = UrlFetchApp.fetch(file.download_url, { headers }).getContentText();
      Logger.log(`Content of ${file.name}:\n${fileContent}`);
      const tables = extractTablesFromClauses(fileContent);
      tables.forEach(table => {
        const tableParts = table.split('.').map(part => part.replace(/`/g, ''));
        const newEntry = [file.name, ...tableParts].join(',');
        if (!existingEntries.has(newEntry)) {
          sheet.getRange(row, 1).setValue(file.name);
          tableParts.forEach((part, index) => {
            sheet.getRange(row, index + 2).setValue(part);
          });
          row++;
        }
      });
    }
  });
}

function extractTablesFromClauses(query) {
  const withClauseRegex = /WITH\s+([a-zA-Z0-9_]+)\s+AS\s+\(/gi;
  const withTables = new Set();
  let match;
  while ((match = withClauseRegex.exec(query)) !== null) {
    withTables.add(match[1]);
  }

  const tableRegex = /(?:FROM|JOIN)\s+`([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)`/gi;
  const tables = [];
  while ((match = tableRegex.exec(query)) !== null) {
    const table = match[1].replace(/`/g, '').trim();
    if (!withTables.has(table)) {
      tables.push(table);
    }
  }
  return tables;
}

function parseEnvFile(filePath) {
  const env = UrlFetchApp.fetch(filePath).getContentText();
  const lines = env.split('\n');
  const envVars = {};
  lines.forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
      envVars[key.trim()] = value.trim().replace(/"/g, '');
    }
  });
  return envVars;
}

function setEnvVariables() {
  const env = `
    GITHUB_ACCESS_TOKEN=your-github-access-token
  `;
  const lines = env.trim().split('\n');
  lines.forEach(line => {
    const [key, value] = line.split('=');
    PropertiesService.getScriptProperties().setProperty(key.trim(), value.trim());
  });
}

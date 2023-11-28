export function dateTime2Text(date_time) {
  const date = date_time.toLocaleDateString(
    'pt-br',
    {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit'
    }
  );
  const time = date_time.toLocaleTimeString('pt-br');
  return date + ' ' + time;
}

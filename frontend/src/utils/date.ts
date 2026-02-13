const DATE_ONLY_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export function parseDate(dateInput: string): Date {
  if (DATE_ONLY_PATTERN.test(dateInput)) {
    const [year, month, day] = dateInput.split("-").map(Number);
    return new Date(year, month - 1, day);
  }

  return new Date(dateInput);
}

export function formatDate(dateInput: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(parseDate(dateInput));
}

export function formatWeekday(dateInput: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    weekday: "short",
  })
    .format(parseDate(dateInput))
    .replace(".", "");
}


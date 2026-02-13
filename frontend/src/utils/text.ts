export function plainTextFromHtml(input: string): string {
  if (!input) {
    return "";
  }

  if (typeof DOMParser !== "undefined") {
    const doc = new DOMParser().parseFromString(input, "text/html");
    const text = doc.body.textContent ?? "";
    return text.replace(/\s+/g, " ").trim();
  }

  return input.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}


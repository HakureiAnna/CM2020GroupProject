export function sanitizeDate(date) {
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    let day = date.getDate();
    const date_string = `${year}/${month}/${day}`;

    return date_string;
}
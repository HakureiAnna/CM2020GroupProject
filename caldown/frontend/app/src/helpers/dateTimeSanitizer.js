// Takes in a date-time string returned from Vue-datepicker plugin
// Returns in the format of "yyyy/mm/dd"

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
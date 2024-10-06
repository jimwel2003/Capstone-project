$(document).ready(function() {
    // Array of disabled dates (year-month-day format)
    var disabledDates = ['2024-09-18', '2024-09-19', '2024-09-20'];
  
    $('.datepicker').datepicker({
        dateFormat: 'yy-mm-dd',
        minDate: 0, // Disable past dates
        beforeShowDay: function(date) {
        var year = date.getFullYear();
        var month = date.getMonth() + 1; // Adjust for 0-based months
        var day = date.getDate();
  
        // Convert date to year-month-day format for comparison
        var formattedDate = year + '-' + (month < 10 ? '0' + month : month) + '-' + (day < 10 ? '0' + day : day);
  
        // Check if the date is in the disabledDates array
        return $.inArray(formattedDate, disabledDates) === -1 ? [true, '', ''] : [false, '', 'disabled'];
      }
    });
});
function getSumPoints(row, col) {
	Logger.log("row: " + row);
	var row = SpreadsheetApp.getActiveSheet().getCurrentCell().getRow();

	if (row >= 24) {
		numGames = 42;
	} else {
		numGames = 38
	}

	sum = 100;
	for (var col = 7; col < 7 + numGames; col++) {
		var value = SpreadsheetApp.getActiveSheet().getRange(row, col).getValue();

		if (value == "-" || value == "APLZ") {
			continue;
		} else if (typeof (value) != "number") {
			Logger.log("Not number: " + value);
			var regExpAPLZJ = new RegExp("APLZ J..");
			var firstRegExp = value.replace(regExpAPLZJ, "");
			var regExpADLJ = new RegExp("ADL J..");
			var secondRegExp = firstRegExp.replace(regExpADLJ, "");
			var regExpComma = new RegExp(",");
			var thirdRegExp = secondRegExp.replace(regExpComma, ".");

			Logger.log("parseFloat: " + parseFloat(thirdRegExp));
			sum += parseFloat(thirdRegExp) - 1.5;
		} else {
			sum += parseFloat(value) - 1.5;
		}
	}

	Logger.log("sum: " + sum);

	return sum;
}

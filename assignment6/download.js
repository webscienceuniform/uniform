var dts = $(".mw-headline").parent().siblings("dl").find("dt")

dts.each((i, elem) => {
  console.log($(elem).text())
})
// fir chhinease

var trs = $(".mw-headline").parent().siblings("table").find("tr")

trs.each((i, elem) => {
  console.log($(elem).find("td").first().text());
})

var k = new Set()


var k = $(".mw-headline").parent().siblings("ul").first().find("li")
k.each((i, elem) => {
  console.log($(elem).find("a:first").text())
})

var lis = $("#mw-content-text").find("ul").first().find("li")

lis.each((i, elem) => {
  console.log($(elem).find("a").first().text())
});

var lis = $("#mw-content-text").find("dl").find("dt")

lis.each((i, elem) => {
  console.log($(elem).find("a").first().text())
});


var lis = $(".mw-headline").parent().siblings("ul").find("li")

lis.each((i, elem) => {
  console.log($(elem).find("a").first().text())
})

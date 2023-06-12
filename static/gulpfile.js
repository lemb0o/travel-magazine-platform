var gulp = require("gulp");
var sass = require("gulp-sass");


gulp.task("default", function() {
    gulp.src('./sass/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('./css/'))
});

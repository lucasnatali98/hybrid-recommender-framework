const gulp = require('gulp');
const ts = require('gulp-typescript');
const clean = require('gulp-clean');

const tsProject = ts.createProject('tsconfig.json');

gulp.task('clean', function () {
  return gulp.src('dist', {read: false, allowEmpty: true})
    .pipe(clean());
});

gulp.task('transpile', function () {
  return tsProject.src()
    .pipe(tsProject())
    .js.pipe(gulp.dest(tsProject.config.compilerOptions.outDir));
});

gulp.task('watch', function () {
  gulp.watch(['src/*.ts', 'test/*.test.ts'], gulp.series(['transpile']));
});

gulp.task('default', gulp.series(['clean', 'transpile', 'watch']));

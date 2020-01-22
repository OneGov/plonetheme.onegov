module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    watch: {
      files: [
        'Gruntfile.js',
        'ftw/**/*.js',
        'ftw/**/*.css',
        'ftw/**/*.scss',
        'plonetheme/onegov/**/*.css',
        'plonetheme/onegov/**/*.scss',
        'plonetheme/onegov/**/*.js'
      ],
      tasks: ['cook_resources']
    },
    shell: {
      cook_resources: {
        command: './bin/upgrade recook --all'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('cook_resources', ['shell:cook_resources']);
};

$(".buildinfo").click(function() {
    var buildname = $(this).text();
    $.ajax('/api/get_build/' + buildname)
    .then(function(result){
        //fill table and then get repo url for link
        if (!('error' in result)) {
            $("#build-info-env").html(result['environment']);
            $("#build-info-app").html(result['project_name']);
            $("#build-info-rev").html(result['revision']);
            $("#build-info-commit").html(result['commit']);
            $("#build-info-branch").html(result['branch']);
            $("#build-info-deployed").html(result['deploy_user']);
            $("#build-info-buildname").html(result['build_name']);
            $("#build-info-date").html(result['date']);
            return $.ajax('/api/get_repo_url/' + result['project_name']);
        } else {
            console.log(result['error']);
            return $.Deferred();
        }
    }, function(){
        //stop if can't get api/get_build
        console.log('error get_build');
        return $.Deferred();
    }).then(function(result){
        //add href to commit
        if (!('error' in result)) {
            var commit = $("#build-info-commit").html();
            var url = result['url'] + "/" + commit;
            var tag = "<a href='" + url + "'>" + commit + "</a>"
            $("#build-info-commit").html(tag);
        }
    }, function(){
        //error if can't get api/get_repo_url but pass
        console.log('error get_repo_url');
        return $.when();
    }).then(function(){
        //open modal window
        $("#buildinfoModal").modal('show');
    });
});

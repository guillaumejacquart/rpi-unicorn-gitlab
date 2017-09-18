var list = new Vue({
    el: '#list',
    data: {
        loading: false,
        config: null,
        list: []
    },
    // define methods under the `methods` object
    methods: {
        getConfig: function(callback) {
            var that = this;
            // `this` inside methods points to the Vue instance
            fetch('keys')
                .then(function(response) {
                    var contentType = response.headers.get("content-type");
                    if (contentType && contentType.indexOf("application/json") !== -1) {
                        return response.json().then(function(json) {
                            that.config = json[0];
                            callback(that.config);
                        });
                    }
                    else {
                        console.log("Oops, nous n'avons pas du JSON!");
                    }
                })
        },
        saveConfig: function() {
            var that = this;
            that.loading = true;
            var payload = that.config;

            fetch("keys", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(function(res) {
                    that.loading = false;
                    return res.text(); 
                })
                .then(function(data) { 
                    if(data !== 'ok'){
                        alert(data)
                    };
                    that.getItems();
                })
        },
        getItems: function() {
            var that = this;
            // `this` inside methods points to the Vue instance
            fetch('config')
                .then(function(response) {
                    var contentType = response.headers.get("content-type");
                    if (contentType && contentType.indexOf("application/json") !== -1) {
                        return response.json().then(function(json) {
                            that.list = json;
                        });
                    }
                    else {
                        console.log("Oops, nous n'avons pas du JSON!");
                    }
                })
        },
        saveItems: function() {
            var that = this;
            that.loading = true;
            var payload = that.list;

            fetch("config", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(function(res) {
                    that.loading = false;
                    return res.text(); 
                })
                .then(function(data) { alert(data === 'ok' ? 'Projects saved successfully !' : data) })
        }
    }
})

var conf = new Vue({
    el: '#gitlabConfig',
    data: {
        loading: false,
        config: {}
    },
    // define methods under the `methods` object
    methods: {
        setConfig: function(conf){
          this.config = conf;  
        },
        saveConfig: function() {
            var that = this;
            that.loading = true;
            var payload = that.config;

            fetch("keys", {
                    method: "PUT",
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(function(res) {
                    that.loading = false;
                    return res.text(); 
                })
                .then(function(data) { 
                    if(data !== 'ok'){
                        alert(data)
                    };
                    $('#gitlabConfig').modal('hide')
                    list.getItems();
                })
        }
    }
})

list.getConfig(function(confDb){
    if(!confDb){
        $('#gitlabConfig').modal('show')
    } else{
        conf.config = confDb;
        list.getItems();
    }
})

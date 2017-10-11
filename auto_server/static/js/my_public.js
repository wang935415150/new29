

(function (jq) {
    var requestUrl="";
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function init() {
            $('.loading').removeClass('hide');
            $.ajax({
                url:requestUrl,
                type:'GET',
                data:{},
                dataType:'JSON',
                success:function (response) {
                    initTableHead(response.table_config);
                    initTableBody(response.data_list,response.table_config);
                    $('.loading').addClass('hide');
                },
                error:function(){
                    $('.loading').addClass('hide');
                }
            })
        };
    function initTableHead(table_config) {
            $('#tHead tr').empty();
                $.each(table_config,function(k,conf){
                    var th = document.createElement('th');
                    th.innerHTML = conf.title;
                    $('#tHead tr').append(th);
                })
        };
    function initTableBody(data_list,table_config) {
        $.each(data_list,function (k,row_dict) {
            var tr = document.createElement('tr');
            $.each(table_config,function (kk,vv) {
                var td = document.createElement('td');
                var format_dict={};
                $.each(vv.text.kwargs,function (kkk,vvv) {
                    if(vvv[0] == "@"){
                        var name=vvv.substring(
                            1,vvv.length);format_dict[kkk]=row_dict[name];
                    }else{
                        format_dict[kkk]=vvv;
                    }

                });
                td.innerHTML = vv.text.tpl.format(format_dict);
                $(tr).append(td);
            });
            $('#tBody').append(tr);
        });
    }

        jq.extend({
            'nBList':function (url) {
                requestUrl = url;
                init()
            }
        })

})(jQuery);


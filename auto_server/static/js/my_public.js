

(function (jq) {
    var requestUrl="";
    var GLOBAL_CHOICES_DICT={};
    // function getChoiceNameById(choice_name,id) {
    //     var val;
    //     var status_choices_list=GLOBAL_CHOICES_DICT[choice_name];
    //     $.each(status_choices_list,function (kkkk,vvvv) {
    //         if (id == vvvv[0]){
    //             val = vvvv[1];
    //         }
    //     });
    //     return val;
    // }
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
                    GLOBAL_CHOICES_DICT = response.global_choices_dict;
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
                    if(conf.display){
                        var th = document.createElement('th');
                    th.innerHTML = conf.title;
                    $('#tHead tr').append(th);
                    }

                })
        };
    function initTableBody(data_list,table_config) {
        $.each(data_list,function (k,row_dict) {
            var tr = document.createElement('tr');
            $.each(table_config,function (kk,vv) {
                if(vv.display){
                    var td = document.createElement('td');
                var format_dict={};
                $.each(vv.text.kwargs,function (kkk,vvv) {
                    if(vvv.substring(0,2)=="@@"){
                        var name = vvv.substring(2,vvv.length);
                        var status_choices_list=GLOBAL_CHOICES_DICT[name];
                        $.each(status_choices_list,function (kkkk,vvvv) {
                       if(row_dict[vv.q]==vvvv[0]){
                           format_dict[kkk] = vvvv[1];
                       }     ;
                        });
                    }
                    else if(vvv[0] == "@"){
                        var name=vvv.substring(
                            1,vvv.length);format_dict[kkk]=row_dict[name];
                    }else{
                        format_dict[kkk]=vvv;
                    }

                });
                td.innerHTML = vv.text.tpl.format(format_dict);
                $(tr).append(td);
                }

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


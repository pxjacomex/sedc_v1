from variable.models import Variable,Unidad

class Titulos():
    def titulo_grafico(self,variable):
        consulta=list(Variable.objects.filter(var_id=variable))
        #return consulta[0].get('var_nombre')
        return consulta[0]
    def titulo_unidad(self,variable):
        var=list(Variable.objects.filter(var_id=variable).values())
        uni=list(Unidad.objects.filter(uni_id=var[0].get('uni_id_id')).values())
        return (uni[0].get('uni_sigla')).encode('utf-8')

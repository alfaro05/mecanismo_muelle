from django.shortcuts import render
from . import mechanisms


def index(request):
    return render(request, "interfaz/index.html")

def simulacion(request):
    return render(request, "interfaz/simulacion.html",{"error_flag":False})

def sobre_el_proyecto(request):
    return render(request, "interfaz/sobre_el_proyecto.html")

def resultados(request):
    no_error_flag = True #Flag to handle exceptions
    #Receive the arguments from the user through HTTP method
    try:
        l2=float(request.POST["l2"])
        l3=float(request.POST["l3"])
        omega=float(request.POST["omega"])
        alpha=float(request.POST["alpha"])
        dist=float(request.POST["dist"])
        alt=float(request.POST["alt"])
        theta=float(request.POST["theta"])
    except:
        return render(request, "interfaz/simulacion.html",{"error_flag":True})
    #Create a mechanism object from the imported module
    #using the input from the user
    mecha = mechanisms.Mechanism(theta, l2, l3, l2, alt)
    mecha.set_speed(omega)
    mecha.set_acceleration(alpha)
    positions=mecha.get_positions()
    speed=mecha.get_speeds()
    acceleration=mecha.get_acceleration()
    mecha.create_plot(0,4.7123889)
    can_be_lifted = mecha.can_be_reached
    surface_intersection = mecha.water_intersection
    boat_offset = abs(surface_intersection[0]+dist)
    print(surface_intersection)
    #A dictionary object is created with the results
    #generated by the model. This object is sent to
    #the template to show the results.
    result_dict = {"ax":positions[0][0],"ay":positions[0][1],"bx":positions[1][0],"by":positions[1][1],
                   "cx":positions[2][0],"cy":positions[2][1],"px":positions[3][0], "py":positions[3][1],
                   "v_ax":speed[0][0],"v_ay":speed[0][1],"v_bx":speed[1][0],"v_by":speed[1][1],
                   "v_cx":speed[2][0],"v_cy":speed[2][1],"v_px":speed[3][0],"v_py":speed[3][1],
                   "acc_x":acceleration[0],"acc_y":acceleration[1],"reach_flag":can_be_lifted,
                   "offset":boat_offset,"omega":omega,"alpha":alpha}
    #Loop rounds the results to be more user-friendly.
    
    for key in result_dict.keys():
        result_dict[key]=round(float(result_dict[key]),3)
    
    return render(request, "interfaz/resultados.html",result_dict)

def contacto(request):
    return render(request, "interfaz/contacto.html")

def robot(request):
    return render(request, "interfaz/robot.html")
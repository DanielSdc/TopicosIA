package com.topai.incidenciasestacionamiento.mapper;

import com.topai.incidenciasestacionamiento.dto.response.AutomovilResponseDTO;
import com.topai.incidenciasestacionamiento.dto.response.IncidenciaResponseDTO;
import com.topai.incidenciasestacionamiento.dto.response.PropietarioResponseDTO;
import com.topai.incidenciasestacionamiento.dto.response.UsuarioResponseDTO;
import com.topai.incidenciasestacionamiento.model.Automovil;
import com.topai.incidenciasestacionamiento.model.Incidencia;
import com.topai.incidenciasestacionamiento.model.Propietario;
import com.topai.incidenciasestacionamiento.model.Usuario;

public class Mapper {

    public static AutomovilResponseDTO toDTO (Automovil automovil){
        if(automovil == null) return null;

        return AutomovilResponseDTO.builder()
                .id(automovil.getId())
                .matricula(automovil.getMatricula())
                .marca(automovil.getMarca())
                .modelo(automovil.getModelo())
                .year(automovil.getYear())
                .propietario(toDTO(automovil.getPropietario()))
                .build();
    }

    public static IncidenciaResponseDTO toDTO (Incidencia incidencia){
        if (incidencia == null) return null;

        return IncidenciaResponseDTO.builder()
                .id(incidencia.getId())
                .fecha(incidencia.getFecha())
                .latitud(incidencia.getLatitud())
                .longitud(incidencia.getLongitud())
                .automovil(toDTO(incidencia.getAutomovil()))
                .usuario(toDTO(incidencia.getUsuario()))
                .build();
    }

    public static UsuarioResponseDTO toDTO(Usuario usuario) {
        if (usuario == null) return null;

        return UsuarioResponseDTO.builder()
                .id(usuario.getId())
                .nombre(usuario.getNombre())
                .correo(usuario.getCorreo())
                .role(usuario.getRole())
                .propietario(toDTO(usuario.getPropietario()))
                .build();
    }

    public static PropietarioResponseDTO toDTO(Propietario propietario){

        if (propietario == null) return  null;

        return PropietarioResponseDTO.builder()
                .id(propietario.getId())
                .nombre(propietario.getNombre())
                .direccion(propietario.getDireccion())
                .correoUsuario(propietario.getUsuario() != null ? propietario.getUsuario().getCorreo() : null)
                .tarjetaPase(propietario.isTarjetaPase())
                .build();
    }


}

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: albaranes_articulos(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION albaranes_articulos(p_id_albaranes integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    recArticulos RECORD;
    resultado INTEGER;
BEGIN
    FOR recArticulos IN SELECT count(*) as count FROM articulos where id_albaranes=p_id_albaranes LOOP
        resultado := recArticulos.count;
    END LOOP;
    RETURN resultado;
END;
$$;


ALTER FUNCTION public.albaranes_articulos(p_id_albaranes integer) OWNER TO postgres;

--
-- Name: albaranes_compra(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION albaranes_compra(p_id_albaranes integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
DECLARE
    recArticulos RECORD;
    resultado FLOAT;
BEGIN
    FOR recArticulos IN SELECT sum(compra) as count FROM articulos where id_albaranes=p_id_albaranes LOOP
        resultado := recArticulos.count;
    END LOOP;
    RETURN resultado;
END;
$$;


ALTER FUNCTION public.albaranes_compra(p_id_albaranes integer) OWNER TO postgres;

--
-- Name: facturas_articulos(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION facturas_articulos(p_id_facturas integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    recArticulos RECORD;
    resultado INTEGER;
BEGIN
    FOR recArticulos IN SELECT count(*) as count FROM articulos where id_facturas=p_id_facturas LOOP
        resultado := recArticulos.count;
    END LOOP;
    RETURN resultado;
END;
$$;


ALTER FUNCTION public.facturas_articulos(p_id_facturas integer) OWNER TO postgres;

--
-- Name: facturas_venta(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION facturas_venta(p_id_facturas integer) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
DECLARE
    recArticulos RECORD;
    resultado FLOAT;
BEGIN
    resultado:=0;
    FOR recArticulos IN select round(sum(venta)::numeric,2) as total from articulos where id_facturas=p_id_facturas LOOP
        resultado := recArticulos.total;
    END LOOP;
    RETURN resultado;
END;
$$;


ALTER FUNCTION public.facturas_venta(p_id_facturas integer) OWNER TO postgres;

--
-- Name: seq_albaranes; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_albaranes
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_albaranes OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: albaranes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE albaranes (
    id_albaranes integer DEFAULT nextval('seq_albaranes'::regclass) NOT NULL,
    fecha date DEFAULT now() NOT NULL,
    id_proveedores integer NOT NULL,
    inventariado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.albaranes OWNER TO postgres;

--
-- Name: seq_articulos; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_articulos
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_articulos OWNER TO postgres;

--
-- Name: articulos; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articulos (
    id_articulos integer DEFAULT nextval('seq_articulos'::regclass) NOT NULL,
    id_albaranes integer NOT NULL,
    id_facturas integer,
    modelo text,
    numeroserie text,
    compra double precision NOT NULL,
    venta double precision NOT NULL,
    id_tipos integer NOT NULL
);


ALTER TABLE public.articulos OWNER TO postgres;

--
-- Name: seq_clientes; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_clientes
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_clientes OWNER TO postgres;

--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE clientes (
    id_clientes bigint DEFAULT nextval('seq_clientes'::regclass) NOT NULL,
    nombre text,
    apellidos text,
    telefono text,
    email text,
    direccion text,
    ciudad text,
    codigopostal text,
    pais text,
    nif text
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: seq_facturas; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_facturas
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_facturas OWNER TO postgres;

--
-- Name: facturas; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE facturas (
    id_facturas integer DEFAULT nextval('seq_facturas'::regclass) NOT NULL,
    id_clientes integer NOT NULL,
    id_usuarios integer,
    hora timestamp without time zone DEFAULT now() NOT NULL,
    pagado boolean DEFAULT false NOT NULL,
    expirados integer[]
);


ALTER TABLE public.facturas OWNER TO postgres;

--
-- Name: TABLE facturas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE facturas IS 'P';


--
-- Name: COLUMN facturas.pagado; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN facturas.pagado IS '0 cuando no está pagado
1 cuando está pagado
2 cuando ha expirado y se rellena';


--
-- Name: seq_proveedores; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_proveedores
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_proveedores OWNER TO postgres;

--
-- Name: proveedores; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE proveedores (
    id_proveedores integer DEFAULT nextval('seq_proveedores'::regclass) NOT NULL,
    proveedor text NOT NULL,
    cif text,
    telefono text,
    email text,
    direccion text,
    ciudad text,
    codigopostal text,
    pais text
);


ALTER TABLE public.proveedores OWNER TO postgres;

--
-- Name: seq_tipos; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_tipos
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_tipos OWNER TO postgres;

--
-- Name: seq_usuarios; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seq_usuarios
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_usuarios OWNER TO postgres;

--
-- Name: tipos; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tipos (
    id_tipos bigint DEFAULT nextval('seq_tipos'::regclass) NOT NULL,
    tipo text NOT NULL
);


ALTER TABLE public.tipos OWNER TO postgres;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE usuarios (
    id_usuarios integer DEFAULT nextval('seq_usuarios'::regclass) NOT NULL,
    usuario text NOT NULL,
    administrador boolean DEFAULT false NOT NULL,
    comercial boolean DEFAULT false NOT NULL,
    gerente boolean DEFAULT false NOT NULL,
    consejoadministracion boolean DEFAULT false NOT NULL,
    contry text
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: pk_albaranes; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY albaranes
    ADD CONSTRAINT pk_albaranes PRIMARY KEY (id_albaranes);


--
-- Name: pk_articulos; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articulos
    ADD CONSTRAINT pk_articulos PRIMARY KEY (id_articulos);


--
-- Name: pk_clientes; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY clientes
    ADD CONSTRAINT pk_clientes PRIMARY KEY (id_clientes);


--
-- Name: pk_facturas; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY facturas
    ADD CONSTRAINT pk_facturas PRIMARY KEY (id_facturas);


--
-- Name: pk_proveedores; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY proveedores
    ADD CONSTRAINT pk_proveedores PRIMARY KEY (id_proveedores);


--
-- Name: pk_tipos; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tipos
    ADD CONSTRAINT pk_tipos PRIMARY KEY (id_tipos);


--
-- Name: pk_usuarios; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY usuarios
    ADD CONSTRAINT pk_usuarios PRIMARY KEY (id_usuarios);


--
-- Name: fk_id_proveedores; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY albaranes
    ADD CONSTRAINT fk_id_proveedores FOREIGN KEY (id_proveedores) REFERENCES proveedores(id_proveedores) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: id_albaranes; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articulos
    ADD CONSTRAINT id_albaranes FOREIGN KEY (id_albaranes) REFERENCES albaranes(id_albaranes) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: id_clientes; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY facturas
    ADD CONSTRAINT id_clientes FOREIGN KEY (id_clientes) REFERENCES clientes(id_clientes) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: id_facturas; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articulos
    ADD CONSTRAINT id_facturas FOREIGN KEY (id_facturas) REFERENCES facturas(id_facturas) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: id_tipos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articulos
    ADD CONSTRAINT id_tipos FOREIGN KEY (id_tipos) REFERENCES tipos(id_tipos) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: id_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY facturas
    ADD CONSTRAINT id_usuarios FOREIGN KEY (id_usuarios) REFERENCES usuarios(id_usuarios) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: proveedores; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE proveedores FROM PUBLIC;
REVOKE ALL ON TABLE proveedores FROM postgres;
GRANT ALL ON TABLE proveedores TO postgres;
GRANT SELECT ON TABLE proveedores TO "gnuopticsComercial";


--
-- Name: tipos; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE tipos FROM PUBLIC;
REVOKE ALL ON TABLE tipos FROM postgres;
GRANT ALL ON TABLE tipos TO postgres;
GRANT SELECT ON TABLE tipos TO "gnuopticsComercial";


--
-- PostgreSQL database dump complete
--

